import { createTheme, CssBaseline, ThemeProvider } from "@mui/material";
import { AlbumListPage } from "./pages/AlbumListPage"
import { FullAlbumPage } from "./pages/FullAlbumPage";
import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
  const theme = createTheme({
  palette: {
    mode: "dark",
    primary: {
      main: "#698194ff",
    },
  },
  shape: {
    borderRadius: 12,
  },
  });
  
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline/>
      <BrowserRouter>
        <Routes>
          <Route path="/albums" element={<AlbumListPage/>} />
          <Route path="/albums/:id" element={<FullAlbumPage/>}/>
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App
