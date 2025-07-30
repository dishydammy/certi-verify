import { Route, Routes } from 'react-router';
import Home from './pages/Home';
import Login from './pages/authentication/login';
import Register from './pages/authentication/register';
import UserDashboard from './pages/authorised_pages/user_dashboard';
import './App.css'

function App() {
 

  return (
    <>
    <Routes>
      <Route element={<Home />} path='/'/>
      <Route element={<Login />} path='/login'/>
      <Route element={<Register />} path='/register'/>
      <Route element={<UserDashboard />} path='/dashboard'/>

    </Routes>
    </>
  )
}

export default App
