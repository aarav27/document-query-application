import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import '@/styles/index.css'
import App from '@/App.tsx'
import { Provider } from "@/components/ui/provider"
import { LoadingProvider } from "@/context/LoadingContext"

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Provider>
      <LoadingProvider>
        <App />
      </LoadingProvider>
    </Provider>
  </StrictMode>
)