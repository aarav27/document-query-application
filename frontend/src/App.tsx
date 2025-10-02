import { useEffect, useState } from 'react'
import { Table } from "@chakra-ui/react"
import './App.css'

interface RecordType {
  document_name: string;
  category: string;
}

function App() {
  const [records, setRecords] = useState<RecordType[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    const fetchRecords = async() => {
      try{
        const response = await fetch("http://127.0.0.1:8000/records")
        if (!response.ok){
          throw new Error(`Error Status: ${response.status}`)
        }
        const data = await response.json()
        setRecords(data)
      } catch {
        setError(true)
        return new Error("Request Failed")
      } finally {
        setLoading(false)
      }
    }
    fetchRecords()
  }, [])

  if(loading){
    return <div></div>
  }
  else if(error){
    return <div>Error</div>
  }
  return (
    <div>
      <h1>
        Document Dashboard
      </h1>
      <div id="table-dashboard">
        <Table.Root>
          <Table.Header>
            <Table.Row>
              <Table.ColumnHeader>Document Name</Table.ColumnHeader>
              <Table.ColumnHeader>Category</Table.ColumnHeader>
              <Table.ColumnHeader>View Document</Table.ColumnHeader>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {records.map((record) => (
              <Table.Row>
                <Table.Cell>{record.document_name}</Table.Cell>
                <Table.Cell>{record.category}</Table.Cell>
                <button>View</button>
              </Table.Row>
            ))}
          </Table.Body>
        </Table.Root>
      </div>
    </div>
  )
  

}

export default App
