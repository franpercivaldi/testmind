import React from 'react';
import { ConfigProvider, Layout, theme } from 'antd';
import StepsComponent from './components/StepsComponent.jsx';

const { Content } = Layout;

function App() {
  return (
    <ConfigProvider
      theme={{
        algorithm: theme.darkAlgorithm,
        token: {
          colorPrimary: '#10a37f',
          colorBgBase: '#0d0d0d',
          colorBgContainer: '#1e1e1e',
          colorBorder: '#333333',
          colorTextBase: '#e5e5e5',
          colorTextTertiary: '#8e8e8e',
        },
      }}
    >
      <Layout style={{ minHeight: '100vh', minWidth: '100vw', padding: '24px', background: '#0d0d0d' }}>
        <Content
          style={{
            width: '100%',
            padding: '24px',
            background: '#1e1e1e',
            borderRadius: '8px',
          }}
        >
          <StepsComponent />
        </Content>
      </Layout>
    </ConfigProvider>
  );
}

export default App;
