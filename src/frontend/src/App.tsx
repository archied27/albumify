import { createTheme, CssBaseline, ThemeProvider } from "@mui/material";
import { AlbumListPage } from "./pages/AlbumListPage"
import { FullAlbumPage } from "./pages/FullAlbumPage";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ClusterAlbumListPage } from "./pages/ClusterAlbumsPage";
import { ClusterListPage } from "./pages/ClusterListPage";
import { TopBar } from "./components/TopBar";
import { SearchListPage } from "./pages/SearchListPage";

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
        <TopBar/>
        <Routes>
          <Route path="/" element={<AlbumListPage/>} />
          <Route path="/albums/:id" element={<FullAlbumPage/>}/>
          <Route path="/clusters" element={<ClusterListPage/>} />
          <Route path="/clusters/:id" element={<ClusterAlbumListPage/>}/>
          <Route path="/search" element={<SearchListPage/>} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App
