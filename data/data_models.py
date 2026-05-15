from typing import Optional
import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, Text, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Tasks(Base):
    __tablename__ = 'tasks'
    __table_args__ = (
        CheckConstraint('is_completed IN (0,1)'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    create_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    followup_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    last_followup: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    is_completed: Mapped[Optional[int]] = mapped_column(Integer)

    notes: Mapped[list['Notes']] = relationship('Notes', back_populates='task')
    time_tracking: Mapped[list['TimeTracking']] = relationship('TimeTracking', back_populates='task')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,

        }


class Notes(Base):
    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    create_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'), nullable=False)
    note: Mapped[Optional[str]] = mapped_column(Text)

    task: Mapped['Tasks'] = relationship('Tasks', back_populates='notes')


class TimeTracking(Base):
    __tablename__ = 'time_tracking'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'), nullable=False)
    start_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    end_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    task: Mapped['Tasks'] = relationship('Tasks', back_populates='time_tracking')
