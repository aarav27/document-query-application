import { Link, useLocation } from "react-router-dom";
import '@/styles/navbar.css'

export default function Navbar(){
    const location = useLocation();

    const linkStyle = (path: string) => ({
        textDecoration: "none",
        color: location.pathname === path ? "#007bff" : "#333",
        fontWeight: location.pathname === path ? "bold" : "normal",
        fontSize: "1.2rem",
        padding: "0.5rem 2.5rem",
        transition: "color 0.2 ease",
    })

    return (
        <nav>
            <Link to='/' style={linkStyle('/')}>Home</Link>
            <Link to='/search' style={linkStyle('/search')}>Search</Link>
            <Link to='/qna' style={linkStyle('/qna')}>Q&A</Link>
        </nav>
    )
}