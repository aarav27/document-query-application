import { useState } from 'react';
import Loader from '@/components/Loader';
import { LoadingContext } from './loading-context';

export function LoadingProvider({ children }: { children: React.ReactNode }) {
  const [loading, setLoading] = useState(false);

  return (
    <LoadingContext.Provider
      value={{
        showLoader: () => setLoading(true),
        hideLoader: () => setLoading(false),
      }}
    >
      {children}
      {loading && <Loader />}
    </LoadingContext.Provider>
  );
}
