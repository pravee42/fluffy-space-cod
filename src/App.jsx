import React, { useEffect, useState } from 'react';
import data from './data.json'
import { DataGrid } from '@mui/x-data-grid';
import { Container, Typography, Button } from '@mui/material';

const columns = [
  { field: 'id', headerName: 'ID', width: 90 },
  {
    field: 'images',
    headerName: 'Images',
    width: 200,
    renderCell: (params) => (
      <div>
        {params.row.images.slice(0, 3).map((image, index) => (
          <img key={index} src={image.s} alt={`product-${index}`} style={{ width: 50, height: 50, marginRight: 5 }} />
        ))}
      </div>
    )
  },
  { field: 'desc', headerName: 'Description', width: 300 },
  { field: 'w', headerName: 'Weight', width: 100 },
  { field: 'brand', headerName: 'Brand', width: 150, renderCell: (params) => <p>{params.row.brand.name}</p> },
  { field: 'category', headerName: 'Category', width: 250, renderCell: (params) => <p>{params.row.category.tlc_name}</p> },
  { field: 'price', headerName: 'Price', width: 110, renderCell: (params) => <p>{params.row.pricing.discount.subscription_price}</p> },
  { field: 'discount', headerName: 'Discount', width: 130, renderCell: (params) => <p>{params.row.pricing.discount.d_text}</p> },
];

function App() {
  const [selectedProducts, setSelectedProducts] = useState([]);

  const handleSelectionModelChange = (newSelection) => {
    setSelectedProducts(newSelection);
    console.log(newSelection);
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        BigBasket Products
      </Typography>
      <div style={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={data.tabs[0].product_info.products}
          columns={columns}
          pageSize={10}
          checkboxSelection
          onSelectionModelChange={handleSelectionModelChange}
        />
      </div>
      <Button onClick={_ => console.log(selectedProducts)}>Save Selected Products</Button>
    </Container>
  );
}

export default App;
