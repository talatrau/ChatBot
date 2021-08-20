import React from 'react'
import Header from './components/Header';
import Content from './components/Content';

const App = () => {
    return (
        <div style={{height:'100vh', width:'100%'}}>
            <Header  />
            <Content />
        </div>
    );
}

export default App;