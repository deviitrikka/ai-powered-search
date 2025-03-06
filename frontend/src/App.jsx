import React, { useState } from "react";
import axios from "axios";
import {
  Container,
  TextField,
  Button,
  CircularProgress,
  Typography,
  Alert,
  Stack,
  Box,
  Card,
  CardMedia,
  CardContent,
} from "@mui/material";
import { FaSearch } from "react-icons/fa";

const App = () => {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [googleResults, setGoogleResults] = useState(null);
  const [youtubeResults, setYoutubeResults] = useState(null);
  const [linkedinResults, setLinkedinResults] = useState(null);
  const [error, setError] = useState(null);

  const handleSearch = async (searchQuery) => {
    const searchText = searchQuery || query.trim();
    if (!searchText) return;
    setLoading(true);
    setError(null);
    setResults(null);
    setGoogleResults(null);
    setYoutubeResults(null);
    setLinkedinResults(null);

    try {
      // Fetch AI-generated relevant queries
      const aiResponse = await axios.get("http://localhost:5000/relevant_queries/", {
        params: { query: searchText },
      });

      if (aiResponse.data?.queries) {
        setResults(aiResponse.data);
      } else {
        setError("Unexpected AI response format");
      }

      // Fetch Google search results
      const googleResponse = await axios.get("http://localhost:5000/google_search/", {
        params: { query: searchText },
      });

      if (googleResponse.data?.results) {
        setGoogleResults(googleResponse.data.results);
      } else {
        setError("Unexpected Google API response format");
      }

      // Fetch YouTube search results
      const youtubeResponse = await axios.get("http://localhost:5000/youtube_search/", {
        params: { query: searchText },
      });

      if (youtubeResponse.data?.results) {
        setYoutubeResults(youtubeResponse.data.results);
      } else {
        setError("Unexpected YouTube API response format");
      }

      // Fetch LinkedIn search results
      const linkedinResponse = await axios.get("http://localhost:5000/linkedin_search/", {
        params: { query: searchText },
      });

      if (linkedinResponse.data?.jobs) {  // Ensure the response key is "jobs"
        setLinkedinResults(linkedinResponse.data.jobs);
      } else {
        setError("Unexpected LinkedIn API response format");
      }
    } catch (err) {
      console.error("Error fetching search results:", err);
      setError("Failed to fetch results. Please try again later.");
    }

    setLoading(false);
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" align="center" gutterBottom>
        🔍 AI, Google, YouTube & LinkedIn Search
      </Typography>

      {/* Search Input Section */}
      <Stack direction="row" spacing={2} alignItems="center" justifyContent="center" sx={{ mt: 2 }}>
        <Box sx={{ flexGrow: 1, maxWidth: "500px" }}>
          <TextField
            fullWidth
            label="Enter your search query..."
            variant="outlined"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          />
        </Box>
        <Button variant="contained" color="primary" onClick={() => handleSearch()} startIcon={<FaSearch />}>
          Search
        </Button>
      </Stack>

      {/* Loading Indicator */}
      {loading && (
        <Box sx={{ textAlign: "center", mt: 3 }}>
          <CircularProgress />
        </Box>
      )}

      {/* Error Message */}
      {error && (
        <Alert severity="error" sx={{ mt: 3 }}>
          {error}
        </Alert>
      )}

      {/* Relevant Queries */}
      {results?.queries?.length > 0 && (
        <Box sx={{ mt: 3, textAlign: "center" }}>
          <Typography variant="h6">💡 Try these relevant queries:</Typography>
          <Stack direction="row" spacing={2} justifyContent="center" flexWrap="wrap" sx={{ mt: 2 }}>
            {results.queries.map((suggestion, index) => (
              <Button key={index} variant="outlined" onClick={() => handleSearch(suggestion)}>
                {suggestion}
              </Button>
            ))}
          </Stack>
        </Box>
      )}

      {/* Google Results */}
      {googleResults && (
        <Box sx={{ mt: 3 }}>
          <Typography variant="h6">🔎 Google Search Results:</Typography>
          <Stack spacing={2} sx={{ mt: 2 }}>
            {googleResults.map((result, index) => (
              <Box key={index} sx={{ border: "1px solid #ddd", p: 2, borderRadius: 2 }}>
                <Typography variant="subtitle1">
                  <a href={result.link} target="_blank" rel="noopener noreferrer">
                    {result.title}
                  </a>
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  {result.snippet}
                </Typography>
              </Box>
            ))}
          </Stack>
        </Box>
      )}

      {/* YouTube Results */}
      {youtubeResults && (
        <Box sx={{ mt: 3 }}>
          <Typography variant="h6">🎥 YouTube Videos:</Typography>
          <Stack spacing={2} sx={{ mt: 2 }}>
            {youtubeResults.map((video, index) => (
              <Card key={index} sx={{ display: "flex", alignItems: "center" }}>
                <CardMedia component="img" sx={{ width: 160, height: 90 }} image={video.thumbnail} alt={video.title} />
                <CardContent>
                  <Typography variant="subtitle1">
                    <a href={`https://www.youtube.com/watch?v=${video.videoId}`} target="_blank" rel="noopener noreferrer">
                      {video.title}
                    </a>
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    {video.channelTitle}
                  </Typography>
                </CardContent>
              </Card>
            ))}
          </Stack>
        </Box>
      )}

      {/* LinkedIn Job Results */}
      {linkedinResults && (
        <Box sx={{ mt: 3 }}>
          <Typography variant="h6">💼 LinkedIn Job Listings:</Typography>

          {loading && (
            <Box sx={{ textAlign: "center", mt: 2 }}>
              <CircularProgress />
            </Box>
          )}

          {!loading && Array.isArray(linkedinResults) && linkedinResults.length > 0 ? (
            <Stack spacing={2} sx={{ mt: 2 }}>
              {linkedinResults.map((job, index) => (
                <Card key={index} sx={{ display: "flex", alignItems: "center", p: 2 }}>
                  <CardContent>
                    <Typography variant="h6">
                      <a href={job.job_link} target="_blank" rel="noopener noreferrer">
                        {job.title}
                      </a>
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      {job.company} - {job.location}
                    </Typography>
                    <Typography variant="caption" color="textSecondary">
                      Posted: {job.posted_time}
                    </Typography>
                  </CardContent>
                </Card>
              ))}
            </Stack>
          ) : (
            <Typography variant="body2" sx={{ mt: 2 }}>
              No job listings found. Try a different query.
            </Typography>
          )}
        </Box>
      )}
    </Container>
  );
};

export default App;
