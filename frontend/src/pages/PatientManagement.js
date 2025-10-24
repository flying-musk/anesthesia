import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Search as SearchIcon,
  Visibility as VisibilityIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { patientAPI } from '../services/api';

const PatientManagement = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [searchOpen, setSearchOpen] = useState(false);
  const [searchData, setSearchData] = useState({
    health_insurance_number: '',
    full_name: '',
    date_of_birth: '',
  });

  // Fetch patients
  const { data: patients = [], isLoading, error } = useQuery(
    'patients',
    () => patientAPI.getPatients().then(res => res.data),
    {
      refetchOnWindowFocus: false,
    }
  );

  // Search patient mutation
  const searchPatientMutation = useMutation(
    (data) => patientAPI.searchPatient(data).then(res => res.data),
    {
      onSuccess: (data) => {
        navigate(`/patients/${data.id}`);
        setSearchOpen(false);
      },
      onError: (error) => {
        console.error('Search failed:', error);
      },
    }
  );

  // Delete patient mutation
  const deletePatientMutation = useMutation(
    (id) => patientAPI.deletePatient(id),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('patients');
      },
    }
  );

  const handleSearch = () => {
    searchPatientMutation.mutate(searchData);
  };

  const handleDelete = (id) => {
    if (window.confirm(t('messages.confirmDelete'))) {
      deletePatientMutation.mutate(id);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const getGenderLabel = (gender) => {
    return t(`patient.genders.${gender}`);
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error">
        {t('errors.networkError')}
      </Alert>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          {t('patient.title')}
        </Typography>
        <Box>
          <Button
            variant="outlined"
            startIcon={<SearchIcon />}
            onClick={() => setSearchOpen(true)}
            sx={{ mr: 2 }}
          >
            {t('patient.searchPatient')}
          </Button>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => navigate('/patients/create')}
          >
            {t('patient.createPatient')}
          </Button>
        </Box>
      </Box>

      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            {t('patient.patientList')}
          </Typography>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>{t('patient.fields.fullName')}</TableCell>
                  <TableCell>{t('patient.fields.healthInsuranceNumber')}</TableCell>
                  <TableCell>{t('patient.fields.dateOfBirth')}</TableCell>
                  <TableCell>{t('patient.fields.gender')}</TableCell>
                  <TableCell>{t('patient.fields.phoneNumber')}</TableCell>
                  <TableCell align="center">{t('app.edit')}</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {patients.map((patient) => (
                  <TableRow key={patient.id}>
                    <TableCell>{patient.full_name}</TableCell>
                    <TableCell>{patient.health_insurance_number}</TableCell>
                    <TableCell>{formatDate(patient.date_of_birth)}</TableCell>
                    <TableCell>
                      <Chip 
                        label={getGenderLabel(patient.gender)} 
                        size="small"
                        color={patient.gender === 'M' ? 'primary' : patient.gender === 'F' ? 'secondary' : 'default'}
                      />
                    </TableCell>
                    <TableCell>{patient.phone_number}</TableCell>
                    <TableCell align="center">
                      <IconButton
                        size="small"
                        onClick={() => navigate(`/patients/${patient.id}`)}
                        title={t('patient.patientDetails')}
                      >
                        <VisibilityIcon />
                      </IconButton>
                      <IconButton
                        size="small"
                        onClick={() => navigate(`/patients/${patient.id}/edit`)}
                        title={t('app.edit')}
                      >
                        <EditIcon />
                      </IconButton>
                      <IconButton
                        size="small"
                        onClick={() => handleDelete(patient.id)}
                        title={t('app.delete')}
                        color="error"
                      >
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Search Dialog */}
      <Dialog open={searchOpen} onClose={() => setSearchOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{t('patient.searchPatient')}</DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2 }}>
            <TextField
              fullWidth
              label={t('patient.fields.healthInsuranceNumber')}
              value={searchData.health_insurance_number}
              onChange={(e) => setSearchData({ ...searchData, health_insurance_number: e.target.value })}
              margin="normal"
            />
            <TextField
              fullWidth
              label={t('patient.fields.fullName')}
              value={searchData.full_name}
              onChange={(e) => setSearchData({ ...searchData, full_name: e.target.value })}
              margin="normal"
            />
            <TextField
              fullWidth
              type="date"
              label={t('patient.fields.dateOfBirth')}
              value={searchData.date_of_birth}
              onChange={(e) => setSearchData({ ...searchData, date_of_birth: e.target.value })}
              margin="normal"
              InputLabelProps={{ shrink: true }}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSearchOpen(false)}>
            {t('app.cancel')}
          </Button>
          <Button
            onClick={handleSearch}
            variant="contained"
            disabled={searchPatientMutation.isLoading}
          >
            {searchPatientMutation.isLoading ? <CircularProgress size={20} /> : t('app.search')}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default PatientManagement;
