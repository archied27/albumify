import { AppBar, Button, Toolbar, Typography, Box, InputBase, IconButton } from "@mui/material";
import { Album, Folder, Person, Search } from "@mui/icons-material";
import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";


const navItems = [
    { label: 'Albums', path: '/', icon: <Album /> },
    { label: 'Clusters', path: '/clusters', icon: <Folder /> },
]

export function TopBar()
{
    const navigate = useNavigate();
    const location = useLocation();
    const [searchOpen, setSearchOpen] = useState(false)
    const [searchQuery, setSearchQuery] = useState('')

    const handleSearch = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && searchQuery.trim()) {
            navigate(`/search?q=${encodeURIComponent(searchQuery.trim())}`)
            setSearchOpen(false)
            setSearchQuery('')
        }
    }

    return (
        <AppBar position="sticky" sx={{ bgcolor: "background.paper" }} elevation={1}>
            <Toolbar sx={{gap:1}}>
                <Typography variant="h6"
                    onClick={() => navigate("/")}
                    sx={{ fontFamily: "-apple-system", cursor: "pointer", mr:2 }}>albumify</Typography>
                
                {navItems.map(item => (
                    <Button key={item.path}
                        onClick={() => navigate(item.path)}
                        sx={{
                            color: location.pathname === item.path ?
                                "primary.main" : "text.secondary",
                                fontWeight: location.pathname === item.path ? 700 : 400
                        }}>{item.icon}</Button>
                ))}

                <Box sx={{ flexGrow: { xs: 1, md: 1 } }} />
                
                {searchOpen ? (
                    <InputBase
                        autoFocus
                        placeholder="Search albums or artists..."
                        value={searchQuery}
                        onChange={e => setSearchQuery(e.target.value)}
                        onKeyDown={handleSearch}
                        onBlur={() => { setSearchOpen(false); setSearchQuery('') }}
                        sx={{
                            bgcolor: 'background.default',
                            px: 2, py: 0.5,
                            borderRadius: 2,
                            width: { xs: '100%', md: 400 },
                            color: 'text.primary',
                            fontSize: 13
                        }}
                    />
                ) : (
                    <IconButton onClick={() => setSearchOpen(true)} sx={{ color: 'text.secondary' }}>
                        <Search />
                    </IconButton>
                )}

                <Button onClick={() => navigate("/user")}
                        sx={{
                            color: location.pathname === "/user" ?
                                "primary.main" : "text.secondary",
                                fontWeight: location.pathname === "/user" ? 700 : 400
                        }}><Person /></Button>

            </Toolbar>
        </AppBar>
    );
}