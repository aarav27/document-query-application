import { createContext } from 'react';

export type LoadingContextType = {
  showLoader: () => void;
  hideLoader: () => void;
};

export const LoadingContext = createContext<LoadingContextType | null>(null);
