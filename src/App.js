

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Bar, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import {
  Container,
  Typography,
  Tabs,
  Tab,
  Box,
  Card,
  CardContent,
  CardHeader,
  Grid,
  Badge,
  Button,
  TextField,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Alert
} from '@mui/material';
import { CheckCircle, Warning, PieChart, Search, BarChart } from '@mui/icons-material';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

const API_URL = 'http://localhost:5000/api';

function App() {
  const [analytics, setAnalytics] = useState(null);
  const [formData, setFormData] = useState({ description: '', amount: '' });
  const [result, setResult] = useState(null);
  const [activeTab, setActiveTab] = useState(0);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const response = await axios.get(`${API_URL}/analytics`);
      setAnalytics(response.data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const analyzeTransaction = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_URL}/categorize`, formData);
      setResult(response.data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const chartData = analytics ? {
    labels: Object.keys(analytics.category_distribution),
    datasets: [{
      data: Object.values(analytics.category_distribution),
      backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
    }]
  } : null;

  const barData = analytics ? {
    labels: Object.keys(analytics.average_amounts),
    datasets: [{
      label: 'Average Amount ($)',
      data: Object.values(analytics.average_amounts),
      backgroundColor: '#36A2EB'
    }]
  } : null;

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h3" align="center" gutterBottom>
        <Badge color="primary" badgeContent={<PieChart />}>
          Financial Transaction Analyzer
        </Badge>
      </Typography>
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 4 }}>
        <Tabs value={activeTab} onChange={(_, v) => setActiveTab(v)} centered>
          <Tab icon={<BarChart />} label="Dashboard" />
          <Tab icon={<Search />} label="Analyze Transaction" />
        </Tabs>
      </Box>

      {activeTab === 0 && analytics && (
        <Box>
          <Grid container spacing={3} mb={2}>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardHeader title="Total Transactions" />
                <CardContent>
                  <Typography variant="h4" color="primary">{analytics.total_transactions}</Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardHeader title="Anomalies" />
                <CardContent>
                  <Typography variant="h4" color="error">{analytics.anomaly_count}</Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardHeader title="Categories" />
                <CardContent>
                  <Typography variant="h4" color="info">{Object.keys(analytics.category_distribution).length}</Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardHeader title="Status" />
                <CardContent>
                  <Typography variant="h4" color="success.main"><CheckCircle /> Active</Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardHeader title="Category Distribution" />
                <CardContent>
                  {chartData && <Pie data={chartData} />}
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={6}>
              <Card>
                <CardHeader title="Average Amounts" />
                <CardContent>
                  {barData && <Bar data={barData} options={{
                    scales: {
                      y: {
                        beginAtZero: true,
                        ticks: {
                          callback: function(value) {
                            return '$' + value.toLocaleString();
                          }
                        }
                      }
                    }
                  }} />}
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          <Box mt={4}>
            <Card>
              <CardHeader title="Recent Transactions" />
              <CardContent>
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Date</TableCell>
                        <TableCell>Description</TableCell>
                        <TableCell>Amount</TableCell>
                        <TableCell>Category</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {analytics.transactions.map((tx, i) => (
                        <TableRow key={i}>
                          <TableCell>{tx.date}</TableCell>
                          <TableCell>{tx.description}</TableCell>
                          <TableCell>${tx.amount}</TableCell>
                          <TableCell><Badge color="primary" badgeContent={tx.category} /></TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </Box>
        </Box>
      )}

      {activeTab === 1 && (
        <Grid container justifyContent="center">
          <Grid item xs={12} md={6}>
            <Card>
              <CardHeader title="Analyze Transaction" />
              <CardContent>
                <Box component="form" onSubmit={analyzeTransaction}>
                  <TextField
                    label="Description"
                    fullWidth
                    margin="normal"
                    value={formData.description}
                    onChange={(e) => setFormData({...formData, description: e.target.value})}
                    placeholder="e.g., PAYROLL DEPOSIT, GROCERY STORE"
                    required
                  />
                  <TextField
                    label="Amount ($)"
                    type="number"
                    fullWidth
                    margin="normal"
                    value={formData.amount}
                    onChange={(e) => setFormData({...formData, amount: e.target.value})}
                    placeholder="0.00"
                    required
                  />
                  <Button type="submit" variant="contained" color="primary" sx={{ mt: 2 }}>Analyze</Button>
                </Box>

                {result && (
                  <Box mt={4}>
                    <Alert severity={result.is_anomaly ? 'error' : 'success'} icon={result.is_anomaly ? <Warning /> : <CheckCircle />}>
                      <Typography variant="h6">Results:</Typography>
                      <Box>
                        <strong>Category:</strong> <Badge color="primary" badgeContent={result.category} />
                      </Box>
                      <Box>
                        <strong>Confidence:</strong> {(result.confidence * 100).toFixed(1)}%
                      </Box>
                      <Box>
                        <strong>Anomaly:</strong> {result.is_anomaly ? '🚨 Anomaly Detected' : '✅ Normal'}
                      </Box>
                    </Alert>
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
    </Container>
  );
}

export default App;
