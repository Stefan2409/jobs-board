import React from 'react';
import './sidebar.scss';
import DashboardIcon from '@mui/icons-material/Dashboard';
import WorkIcon from '@mui/icons-material/Work';
import PeopleIcon from '@mui/icons-material/People';
import BadgeIcon from '@mui/icons-material/Badge';
import logo from './logo.jpg';

const Sidebar = () => {
  return (
    <div className='sidebar'>
        <div className="top">
            <img src={logo} alt="Logo" className="logo" />
        </div>
        <hr />
        <div className="center">
            <ul>
                <p className="title">MAIN</p>
                <li>
                    <DashboardIcon className='icon'/>
                    <span>Dashboard</span>
                </li>
                <p className="title">LISTS</p>
                <li>
                    <PeopleIcon className='icon'/>
                    <span>Users</span>
                </li>
                <li>
                    <WorkIcon className='icon'/>
                    <span>Jobs</span>
                </li>
                <li>
                    <BadgeIcon className='icon'/>
                    <span>Applicants</span>
                </li>
                <p className="title">SYSTEM</p>
                <li>
                    <BadgeIcon className='icon'/>
                    <span>Logs</span>
                </li>
                <li>
                    <BadgeIcon className='icon'/>
                    <span>Settings</span>
                </li>
            </ul>
        </div>
        <div className="bottom">
            <div className="colorOption"></div>
            <div className="colorOption"></div>
        </div>
    </div>
  )
}

export default Sidebar