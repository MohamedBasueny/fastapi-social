"""add foreign key to posts , owner_id col

Revision ID: 0c9205e6d657
Revises: a3603d8e968c
Create Date: 2023-12-13 20:45:32.208865

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column ,Integer 

# revision identifiers, used by Alembic.
revision: str = '0c9205e6d657'
down_revision: Union[str, None] = 'a3603d8e968c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts" , Column("owner_id" , Integer , nullable=False ))
    op.create_foreign_key(constraint_name="fk_posts_owner_id_users" ,
                           ondelete="CASCADE" , 

                           source_table="posts" , 
                           local_cols=["owner_id"] , 

                           referent_table="users" , 
                           remote_cols=["id"]) 

def downgrade() -> None:
    op.drop_constraint(constraint_name="fk_posts_owner_id_users" )
    op.drop_column("posts" , "owner_id")
