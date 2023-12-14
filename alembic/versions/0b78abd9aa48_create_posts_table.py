"""create posts table

Revision ID: 0b78abd9aa48
Revises: 
Create Date: 2023-12-13 19:25:08.679793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b78abd9aa48'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts" , 
                    sa.Column('id' , sa.Integer , primary_key=True , nullable=False) , 
                    sa.Column('title' , sa.String(50), nullable=False)
                    )

def downgrade() -> None:
    op.drop_table('posts')