"""add posts.content column

Revision ID: 397b0b93cc5d
Revises: 0b78abd9aa48
Create Date: 2023-12-13 19:49:24.459004

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column , String 

# revision identifiers, used by Alembic.
revision: str = '397b0b93cc5d'
down_revision: Union[str, None] = '0b78abd9aa48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts" ,Column('content', String(200) , nullable=False
                                  ))

def downgrade() -> None:
    op.drop_column("posts" , "content")