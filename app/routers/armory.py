"""Armory: see gear, buy it with coins, and equip it. Gear is cosmetic only."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..deps import get_current_user, get_db
from ..game.items import get_item
from ..models import Loadout, Unlock, User
from ..schemas import BuyIn, LoadoutIn
from ..views import gear_out, user_out

router = APIRouter(prefix="/api/armory", tags=["armory"])


def _owns(db: Session, user_id: int, item_id: str) -> bool:
    return db.scalar(select(Unlock.id).where(Unlock.user_id == user_id, Unlock.item_id == item_id)) is not None


@router.get("")
def armory(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return {"user": user_out(user), "gear": gear_out(db, user)}


@router.post("/buy")
def buy(data: BuyIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = get_item(data.item_id)
    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such item")
    db.refresh(user, with_for_update=True)   # lock the player's row so coins cannot be spent twice
    if _owns(db, user.id, item["id"]):
        raise HTTPException(status.HTTP_409_CONFLICT, "You already own this item")
    if item["price"] is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "This item is earned by ranking up, not bought")
    if user.coins < item["price"]:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Not enough coins")
    user.coins -= item["price"]
    db.add(Unlock(user_id=user.id, item_id=item["id"]))
    db.commit()
    return {"user": user_out(user), "gear": gear_out(db, user)}


@router.put("/loadout")
def equip(data: LoadoutIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    current = db.get(Loadout, (user.id, data.fighter))
    if data.item_id is None:
        if current is not None:
            db.delete(current)
    else:
        item = get_item(data.item_id)
        if item is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "No such item")
        if item["fighter"] != data.fighter:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "That item belongs to a different fighter")
        if not _owns(db, user.id, item["id"]):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "You have not unlocked this item")
        if current is None:
            db.add(Loadout(user_id=user.id, fighter=data.fighter, item_id=item["id"]))
        else:
            current.item_id = item["id"]
    db.commit()
    return {"user": user_out(user), "gear": gear_out(db, user)}
