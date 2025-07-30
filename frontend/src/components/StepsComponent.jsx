import React, { useState, useEffect } from 'react';
import * as XLSX from 'xlsx';
import {
  Button,
  message,
  Steps,
  theme,
  Upload,
  Typography,
  Space
} from 'antd';
import { UploadOutlined, FolderOpenOutlined } from '@ant-design/icons';
import { Select, Badge, Divider, Table  } from 'antd';
import { uploadFile, listFiles, getJiraIssues, generateTestCases } from '../api/api.js';
import ResultComponent from './ResultComponent';
import SegmentedComponent from './SegmentedComponent';

const { Text, Title } = Typography;

const StepsComponent = () => {
  const { token } = theme.useToken();
  const [current, setCurrent] = useState(0);
  const [uploadSuccess, setUploadSuccess] = useState(null);
  const [uploadMessage, setUploadMessage] = useState('');
  const [testCases, setTestCases] = useState([]);


  // Estados file_id | tickets_id
  const [formState, setFormState] = useState({
    fileId: null,
    ticketIds: [],
  });

  // Estados step 1
  const [step1Mode, setStep1Mode] = useState('upload');
  const [availableFiles, setAvailableFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [loadingFiles, setLoadingFiles] = useState(false);

  // Estados step 2
  const [selectedProject, setSelectedProject] = useState('APISIUCC');
  const [loadingTickets, setLoadingTickets] = useState(false);
  const [jiraIssues, setJiraIssues] = useState([]);

  // Estados step 3
  const [generating, setGenerating] = useState(false);

  const next = () => {
    setCurrent(current + 1);
  };
  const prev = () => {
    setCurrent(current - 1);
  };

  const goToNextStep = () => {
    setCurrent(current + 1);
  };

  const resetUpload = () => {
    setUploadSuccess(null);
    setUploadMessage('');
  };


  // Efecto para inicializar el fileId si ya existe en formState
  useEffect(() => {
    if (formState.fileId && !selectedFile) {
      setSelectedFile(formState.fileId);
    }
  }, [formState.fileId, selectedFile]);

  // Efecto para cargar archivos disponibles al cambiar el modo de step1
  useEffect(() => {
    if (step1Mode === 'select') {
      setLoadingFiles(true);
      listFiles()
        .then((data) => {
          console.log('Archivos disponibles:', data);
          setAvailableFiles(data);
        })
        .catch((err) => {
          console.error('Error al listar archivos:', err);
          message.error('No se pudieron cargar los archivos.');
        })
        .finally(() => setLoadingFiles(false));
    }
  }, [step1Mode]);

  const loadTickets = async () => {
    setLoadingTickets(true);
    try {
      const data = await getJiraIssues({
        projectKey: selectedProject,
        status: 'QA TESTING',
        maxResults: 50,
      });
      setJiraIssues(data);
      console.log('Tickets obtenidos:', data);
      setFormState((prev) => ({
        ...prev,
        ticketIds: data.map((ticket) => ticket.key),
      }));
      message.success(`Se cargaron ${data.length} tickets de Jira.`);
    } catch (err) {
      console.error('Error al cargar tickets:', err);
      message.error('Error al obtener los tickets de Jira.');
    } finally {
      setLoadingTickets(false);
    }
  };

  const handleGenerate = async () => {
    setGenerating(true);
    try {
      const payload = {
        file_id: formState.fileId,
        ticket_ids: formState.ticketIds,
      };

      const result = await generateTestCases(payload);
      setTestCases(result);
      message.success('Casos de prueba generados correctamente.');
      console.log('Respuesta del backend:', result);
    } catch (error) {
      console.error('Error al generar casos:', error);
      message.error('Error al generar casos de prueba.');
    } finally {
      setGenerating(false);
    }
  };


  const exportToExcel = () => {
    const worksheetData = testCases.map((item) => ({
      Fecha: item.fecha,
      Tipo: item.tipo,
      Prioridad: item.prioridad,
      Estado: item.estado,
      Descripción: item.descripcion,
      Precondiciones: item.precondiciones,
      Pasos: item.pasos,
      'Resultado Esperado': item.resultado_esperado,
      'Resultado Actual': item.resultado_actual,
    }));

    const worksheet = XLSX.utils.json_to_sheet(worksheetData);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'CasosDePrueba');

    XLSX.writeFile(workbook, 'casos_de_prueba.xlsx');
  };


  const uploadProps = {
    name: 'file',
    accept: '.xlsx,.xls',
    customRequest: async ({ file, onSuccess, onError }) => {
      try {
        const result = await uploadFile(file);
        setFormState(prev => ({ ...prev, fileId: result.id }));
        setUploadSuccess(true);
        setUploadMessage('Archivo procesado correctamente.');
        onSuccess("ok");
      } catch (error) {
        console.error('Error al subir archivo:', error);
        setUploadSuccess(false);
        setUploadMessage('No se pudo subir el archivo. Intenta nuevamente.');
        onError(error);
      }
    },
    showUploadList: false,
  };

 const step1Content = (
    <div style={{ padding: 24, textAlign: 'center'}}>
      <Space direction="vertical" size="large" style={{ width: '40%' }}>
        <SegmentedComponent
          value={step1Mode}
          onChange={setStep1Mode}
          options={[
            { value: 'upload', label: 'Subir archivo', icon: <UploadOutlined /> },
            { value: 'select', label: 'Seleccionar archivo', icon: <FolderOpenOutlined /> },
          ]}
        />

        {step1Mode === 'upload' ? (
          uploadSuccess !== null ? (
            <ResultComponent
              status={uploadSuccess ? 'success' : 'error'}
              subtitle={uploadMessage}
              onNext={goToNextStep}
              onRetry={resetUpload}
            />
          ) : (
            <Space direction="vertical" size="middle" style={{ width: '100%' }}>
              <Title level={4} style={{ color: token.colorTextBase }}>Sube tu archivo Excel</Title>
              <Text type="secondary">Selecciona un archivo .xlsx desde tu computadora</Text>
              <Upload {...uploadProps}>
                <Button icon={<UploadOutlined />} type="primary">
                  Subir archivo
                </Button>
              </Upload>
            </Space>
          )
        ) : (
          <div>
            <Title level={4} style={{ color: token.colorTextBase }}>Seleccionar archivo existente</Title>
            <Text type="secondary">Selecciona un archivo previamente subido:</Text>
            <Select
              style={{ width: '100%', marginTop: 12 }}
              placeholder="Selecciona un archivo"
              loading={loadingFiles}
              value={selectedFile}
              onChange={(value) => {
                setSelectedFile(value);
                setFormState(prev => ({ ...prev, fileId: value }));
              }}
            >
              {availableFiles.map((f) => (
                <Select.Option key={f.id} value={f.id}>
                  {`${f.original_filename} - ${f.uploaded_at}`}
                </Select.Option>
              ))}
            </Select>

            <Button
              type="primary"
              style={{ marginTop: 16 }}
              disabled={!selectedFile}
              onClick={goToNextStep}
            >
              Siguiente
            </Button>

          </div>
        )}
      </Space>
    </div>
  );

  const step2Content = (
    <div style={{ textAlign: 'center', padding: 24 }}>
      <Space direction="vertical" size="large" style={{ width: '50%' }}>
        <Title level={4} style={{ color: token.colorTextBase }}>Selecciona un proyecto de Jira</Title>

        <SegmentedComponent
          value={selectedProject}
          onChange={setSelectedProject}
          options={[
            { value: 'APISIUCC', label: 'APISIUCC' },
            { value: 'ACCO', label: 'ACCO' },
            { value: 'SW', label: 'SW' },
            { value: 'MS', label: 'MS' },
            { value: 'AUTO', label: 'AUTO' },
          ]}
        />

        <Button type="primary" onClick={loadTickets} loading={loadingTickets}>
          Cargar Tickets
        </Button>

        {jiraIssues.length > 0 && (
          <Text type="success">
            {jiraIssues.length} tickets seleccionados automáticamente para el paso 3.
          </Text>
        )}
      </Space>
    </div>
  );


  const step3Content = (
    <div style={{ padding: 24 }}>
      <Title level={4} style={{ color: token.colorTextBase }}>
        Confirmación de generación de casos
      </Title>

      <Text type="secondary">Se generarán casos de prueba para:</Text>

      <Divider />

      <Text strong>Proyecto seleccionado:</Text>
      <br />
      <Badge color="blue" text={selectedProject} />

      <Divider />

      <Text strong>Tickets seleccionados:</Text>
      <div style={{ marginTop: 8 }}>
        {formState.ticketIds.map((ticket) => (
          <Badge
            key={ticket}
            color="green"
            style={{ marginRight: 8, marginBottom: 8 }}
            text={ticket}
          />
        ))}
      </div>

      <Divider />

      <Button
        type="primary"
        loading={generating}
        onClick={handleGenerate}
        disabled={!formState.fileId || formState.ticketIds.length === 0}
      >
        Generar casos de prueba
      </Button>
      {testCases.length > 0 && (
        <div style={{ marginTop: 32 }}>
          <Title level={5} style={{ color: token.colorTextBase }}>Casos generados:</Title>

          <Table
            dataSource={testCases}
            rowKey="id"
            pagination={{ pageSize: 5 }}
            expandable={{
              expandedRowRender: (record) => (
                <div>
                  <p><strong>Descripción:</strong> {record.descripcion}</p>
                  <p><strong>Precondiciones:</strong> {record.precondiciones}</p>
                  <p><strong>Pasos:</strong><br />{record.pasos?.split('\n').map((p, i) => <div key={i}>{p}</div>)}</p>
                  <p><strong>Resultado esperado:</strong> {record.resultado_esperado}</p>
                  <p><strong>Resultado actual:</strong> {record.resultado_actual}</p>
                </div>
              ),
            }}
            columns={[
              {
                title: 'Fecha',
                dataIndex: 'fecha',
              },
              {
                title: 'Tipo',
                dataIndex: 'tipo',
              },
              {
                title: 'Prioridad',
                dataIndex: 'prioridad',
              },
              {
                title: 'Estado',
                dataIndex: 'estado',
              },
            ]}
          />
          <Button type="default" onClick={exportToExcel} style={{ marginTop: 16 }}>
            Exportar a Excel
          </Button>
        </div>
      )}
    </div>
  );

  // TODO: implementar Tour component para los steps
  const steps = [
    {
      title: 'Subir archivo',
      content: step1Content,
    },
    {
      title: 'Seleccionar opción',
      content: step2Content,
    },
    {
      title: 'Ver resultado',
      content: step3Content,
    },
  ];

  const items = steps.map(item => ({ key: item.title, title: item.title }));

  const contentStyle = {
    minHeight: 260,
    padding: 24,
    color: token.colorTextTertiary,
    backgroundColor: token.colorBgContainer,
    borderRadius: token.borderRadiusLG,
    border: `1px dashed ${token.colorBorder}`,
    marginTop: 16,
  };

  return (
    <>
      <Steps current={current} items={items} />
      <div style={contentStyle}>{steps[current].content}</div>
      <div style={{ marginTop: 24, textAlign: 'center' }}>
        {current > 0 && (
          <Button style={{ margin: '0 8px' }} onClick={prev}>
            Previous
          </Button>
        )}
        {current < steps.length - 1 && (
          <Button type="primary" onClick={next}>
            Next
          </Button>
        )}
      </div>
    </>
  );
};

export default StepsComponent;
