import React from 'react';
import { Segmented } from 'antd';

/**
 * Componente genérico para un segmented control.
 * 
 * @param {string} value - Valor seleccionado actualmente.
 * @param {function} onChange - Callback al cambiar de opción.
 * @param {array} options - Arreglo de objetos: { value, label, icon (opcional) }
 */
const SegmentedComponent = ({ value, onChange, options }) => (
  <Segmented
    value={value}
    onChange={onChange}
    options={options}
    block
  />
);

export default SegmentedComponent;
