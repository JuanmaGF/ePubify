import React, { useState } from 'react';
import axios from 'axios';

const FileUpload = () => {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState('');

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('pdfFile', file);

        try {
            const response = await axios.post('http://localhost:5000/convert', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            setMessage(`Archivo convertido. Puedes descargarlo aquí: ${response.data.fileUrl}`);
        } catch (err) {
            setMessage('Error al convertir el archivo.');
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input type="file" onChange={handleFileChange} />
                <button type="submit">Convertir a EPUB</button>
            </form>
            <p>{message}</p>
        </div>
    );
};

export default FileUpload;
