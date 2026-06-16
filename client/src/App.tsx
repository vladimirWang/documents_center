import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'
import DocumentDetailPage from './pages/DocumentDetailPage'
import DocumentsPage from './pages/DocumentsPage'
import HomePage from './pages/HomePage'
import ClientPage from './pages/ClientPage'
import ClientCreatePage from './pages/ClientCreatePage'
import OrderPage from './pages/OrderPage'
import OrderCreatePage from './pages/OrderCreatePage'
import ProductPage from './pages/ProductPage'
import ProductCreatePage from './pages/ProductCreatePage'
import ProductEditPage from './pages/ProductEditPage'
import ProductBalanceEditPage from './pages/ProductBalanceEditPage'
import FilesPage from './pages/FilesPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route element={<ProtectedRoute />}>
          <Route element={<Layout />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/documents" element={<DocumentsPage />} />
            <Route path="/files" element={<FilesPage />} />
            <Route path="/clients" element={<ClientPage />} />
            <Route path="/clients/new" element={<ClientCreatePage />} />
            <Route path="/products" element={<ProductPage />} />
            <Route path="/orders" element={<OrderPage />} />
            <Route path="/orders/new" element={<OrderCreatePage />} />
            <Route path="/products/new" element={<ProductCreatePage />} />
            <Route path="/products/:id/edit" element={<ProductEditPage />} />
            <Route path="/products/:id/balance" element={<ProductBalanceEditPage />} />
            <Route path="/documents/:id" element={<DocumentDetailPage />} />
          </Route>
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
