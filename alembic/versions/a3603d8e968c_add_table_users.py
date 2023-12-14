"""add table users

Revision ID: a3603d8e968c
Revises: 397b0b93cc5d
Create Date: 2023-12-13 19:58:53.128861

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column , String , Integer , text , TIMESTAMP , Constraint ,ForeignKeyConstraint

# revision identifiers, used by Alembic.
revision: str = 'a3603d8e968c'
down_revision: Union[str, None] = '397b0b93cc5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users" , 
                    Column("id" ,Integer ,primary_key=True) , 
                    Column("email" , String,  unique=True , nullable=False) ,
                    Column("password" , String , nullable=False ),
                    Column("created_at" , TIMESTAMP(timezone=True) , server_default=text("now()") , nullable=False)
                    )

def downgrade() -> None:
    op.drop_table("users")