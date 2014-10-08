from datetime import datetime
from sqlalchemy import Boolean, Column
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Appointment(Base):
   """An appointment on the calendar."""
   __tablename__ = 'appointment'
   id = Column(Integer, primary_key=True)
   created = Column(DateTime, default=datetime.now)
   modified = Column(DateTime, default=datetime.now,
      onupdate=datetime.now)

   title = Column(String(255))
   start = Column(DateTime, nullable=False)
   end = Column(DateTime, nullable=False)
   allday = Column(Boolean, default=False)
   location = Column(String(255))
   description = Column(Text)

   @property
   def duration(self):
      delta = self.end - self.start
      return delta.days * 24 * 60 * 60 + delta.seconds

   def __repr__(self):
      return (u'<{self.__class__.__name__}: {self.id}>'
			.format(self=self))