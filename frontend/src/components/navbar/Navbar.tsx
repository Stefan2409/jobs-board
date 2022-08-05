import React from 'react';
import './navbar.scss';
import SearchIcon from '@mui/icons-material/Search';
import LanguageIcon from '@mui/icons-material/Language';
import NotificationsActiveIcon from '@mui/icons-material/NotificationsActive';
import avatar from './avatar.png';

const Navbar = () => {
  return (
    <div className='navbar'>
      <div className="wrapper">
        <div className="search">
          <input type="text" name='search' placeholder='Search...'/>
          <SearchIcon />
        </div>
        <div className="items">
          <div className="item">
            <LanguageIcon className='icon' />
            English
          </div>
          <div className="item">
            <NotificationsActiveIcon className='icon' />
          </div>
          <div className="item">
            <img src={avatar} alt="Avatar" className='avatar'/>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Navbar