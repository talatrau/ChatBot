import ReactDOM from 'react-dom'
import App from './App'
import Login from './Login'


const user = sessionStorage.getItem('user');

if (user === null) ReactDOM.render(<Login />, document.getElementById('root'));
else ReactDOM.render(<App />, document.getElementById('root'));