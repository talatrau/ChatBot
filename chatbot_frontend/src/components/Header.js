import React from 'react'
import './components.css'

const Header = () => {

    return (
        <div className="header">
            <div className='left'>
                Logo hoặc Thương Hiệu
            </div>

            <a href="." className='right-active'>
                    Chức năng 2
            </a>

            <a href="." className='right-inactive'>
                Chức năng 1
            </a>                      
        </div>
    );
}

export default Header;