import React from 'react'
import ChatFeed from './ChatFeed';
import ChatList from './ChatList';
import ChatInfor from './ChatInfor';
import './components.css'

const Content = () => {
    return (
        <div className="content">
            <ChatList />
            <ChatInfor />
            <ChatFeed />
        </div>
    );
}

export default Content;