"""adding rest of posts columns

Revision ID: cecc3c4d13dd
Revises: 0c9205e6d657
Create Date: 2023-12-13 21:02:09.323252

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column , TIMESTAMP  , Boolean , text

# revision identifiers, used by Alembic.
revision: str = 'cecc3c4d13dd'
down_revision: Union[str, None] = '0c9205e6d657'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts" , 
                  Column("published" , Boolean , server_default="True" , nullable=False ))
    op.add_column("posts" , 
                  Column("created_at" , TIMESTAMP(timezone=True) , nullable=False , 
                         server_default=text("now()") ))

def downgrade() -> None:
    op.drop_column("posts" , "published") 
    op.drop_column("posts" , "created_at") 