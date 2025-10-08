import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom';
import { Table } from "@chakra-ui/react"
import '@/styles/home.css'

interface RecordType {
  document_name: string;
  category: string;
}

export default function HomePage() {
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
      <div className='dashboard-top'>
        <h1 className='dashboard-title'>
          Document Dashboard
        </h1>
        <Link to='/add-document'>
          <button className='add-document-button'>Add Document</button>
        </Link>
      </div>
      <div>
        <Table.Root variant="outline" bg="blue.200">
          <Table.Header className="table-header">
            <Table.Row>
              <Table.ColumnHeader className="table-cell-header">Document Name</Table.ColumnHeader>
              <Table.ColumnHeader className="table-cell-header">Category</Table.ColumnHeader>
              <Table.ColumnHeader className="table-cell-header">View Document</Table.ColumnHeader>
            </Table.Row>
          </Table.Header>
          <Table.Body className="table-body">
            {records.map((record) => (
              <Table.Row className="table-row">
                <Table.Cell className="table-cell">{record.document_name}</Table.Cell>
                <Table.Cell className="table-cell">{record.category}</Table.Cell>
                <Table.Cell className="table-cell">
                  <button className="table-cell">View</button>
                </Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table.Root>
      </div>
    </div>
  )
  

}