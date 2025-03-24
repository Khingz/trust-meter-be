from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

async def get_all(model, db: AsyncSession):
    result = await db.execute(select(model))
    return result.scalars().all()

async def get_by_id(model, model_id, db: AsyncSession):
    result = await db.execute(select(model).filter_by(id=model_id))
    return result.scalar()

async def create(instance, db: AsyncSession):
    db.add(instance)
    await db.commit()
    await db.refresh(instance)
    return instance

async def delete(instance, db: AsyncSession):
    await db.delete(instance)
    await db.commit()




if __name__ == "__main__":
    from session import get_db
    from models import Product

    db = next(get_db())  # Initialize the database session
    sample_data = {
        "name": "Sample Product",
        "description": "This is a test product",
        "price": 9.99,
    }
    # create_product(db, sample_data)
