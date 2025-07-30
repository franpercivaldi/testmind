import React from 'react';
import { Button, Result } from 'antd';

const ResultComponent = ({ status, subtitle, onNext, onRetry }) => (
  <Result
    status={status}
    title={status === 'success' ? 'Archivo subido con éxito!' : 'Error al subir archivo'}
    subTitle={subtitle}
    extra={[
      <Button type="primary" key="next" onClick={onNext}>
        Siguiente
      </Button>,
      <Button key="retry" onClick={onRetry}>
        Subir otro archivo
      </Button>,
    ]}
  />
);

export default ResultComponent;
