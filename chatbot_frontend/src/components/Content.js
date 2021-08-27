import React from 'react'
import ChatFeed from './ChatFeed';
import ChatList from './ChatList';
import ChatInfor from './ChatInfor';
import './components.css'

const Content = () => {
    const user = sessionStorage.getItem('user');

    return (
        <div className="content">
            <ChatList user={user} />
            <ChatInfor user={user} />
            <ChatFeed user={user} topic='fashion' />
        </div>
    );
}

export default Content;