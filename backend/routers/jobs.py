from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select, Session
from ..database import engine, get_session
from ..models.jobs import JobsCreate, JobsRead, Job, JobsUpdate, JobReadWithOccupationGroup
from typing import List

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
)


@router.get("/", response_model=List[JobsRead])
async def get_jobs(*, session: Session = Depends(get_session), offset: int = 0, limit: int = Query(default=100, lte=100)):
    jobs = session.exec(select(Job).offset(offset).limit(limit)).all()
    return jobs


@router.get("/{job_id}", response_model=JobReadWithOccupationGroup)
async def get_job(*, session: Session = Depends(get_session), job_id: int):
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/", response_model=JobsRead)
async def create_job(*, session: Session = Depends(get_session), job: JobsCreate):
    db_job = Job.from_orm(job)
    session.add(db_job)
    session.commit()
    session.refresh(db_job)
    return db_job


@router.patch("/{job_id}", response_model=JobsRead)
async def update_job(*, session: Session = Depends(get_session), job_id: int, job: JobsUpdate):
    db_job = session.get(Job, job_id)
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    job_data = job.dict(exclude_unset=True)
    for key, value in job_data.items():
        setattr(db_job, key, value)
    session.add(db_job)
    session.commit()
    session.refresh(db_job)
    return db_job


@router.delete("/{job_id}")
async def delete_job(*, session: Session = Depends(get_session), job_id: int):
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    session.delete(job)
    session.commit()
    return {"ok": True}
