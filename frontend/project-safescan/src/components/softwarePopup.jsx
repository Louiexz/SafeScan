import React, { useEffect, useState } from 'react';
import { createSoftware, updateSoftware } from '../services/softwareService';
import Radio from './inputRadio';
import { useMutation } from 'react-query';
import Modal from 'react-modal'; // Biblioteca para modal
import '../assets/styles/Modal.css';

const PopupSoftware = ({ method, data, onClose, refetch }) => {
  const [softwareName, setSoftwareName] = useState("");
  const [fields, setFields] = useState([
    { name: "localizacao", label: "Software localização", value: false },
    { name: "rede", label: "Software rede", value: false },
    { name: "bluetooth", label: "Software bluetooth", value: false },
    { name: "armazenamento", label: "Software armazenamento", value: false },
    { name: "sistema", label: "Software sistema", value: false },
    { name: "message", label: "Software message", value: false },
    { name: "midia_audio", label: "Software midia-audio", value: false },
    { name: "biblioteca_classes", label: "Software biblioteca-class", value: false },
    { name: "pacotes", label: "Software pacotes", value: false },
  ]);

  const mutationCreateSoftware = useMutation(createSoftware, {
    onSuccess: () => {
      console.log('Software criado com sucesso');
      refetch(); // Trigger refetch after creation
    },
    onError: (error) => console.error('Erro ao criar software:', error),
  });

  const mutationUpdateSoftware = useMutation(updateSoftware, {
    onSuccess: () => {
      console.log('Software atualizado com sucesso');
      refetch(); // Trigger refetch after update
    },
    onError: (error) => console.error('Erro ao atualizar software:', error),
  });

  const getMutationState = (method) =>
    method === 'create' ? mutationCreateSoftware : mutationUpdateSoftware;

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(fields)
    if (!softwareName || fields.some(field => field.value === null || field.value === "")) {
      console.error('Todos os campos precisam ser preenchidos.');
      return;
    }

    const dataToSend = {
      name: softwareName,
      ...Object.fromEntries(fields.map(({ name, value }) => [name, value ? 1 : 0])),
    };

    if (method === "update" && data) {
      dataToSend.id = data.id;
    }

    method === "create"
      ? mutationCreateSoftware.mutate(dataToSend)
      : mutationUpdateSoftware.mutate(dataToSend);
  };

  useEffect(() => {
    if (method === "update" && data) {
      setSoftwareName(data.name || "");
      setFields((prevFields) =>
        prevFields.map((field) => ({
          ...field,
          value: data[field.name] !== undefined ? data[field.name] : null,
        }))
      );
    }
  }, [method, data]);

  const mutation = getMutationState(method);

  return (
    <Modal
      isOpen={true} // Use um estado para controlar a visibilidade
      contentLabel="Software Form"
      ariaHideApp={false} // Para evitar warning do React Modal
    >
      <form onSubmit={handleSubmit} id="form">
        <div>
          <label htmlFor="name">Software name</label>
          <input
            type="text"
            id="name"
            value={softwareName}
            onChange={(e) => setSoftwareName(e.target.value)}
          />
        </div>

        {fields.map(({ name, label, value }) => (
          <Radio
            key={name}
            pergunta={label}
            nome={name}
            value={value}
            onchange={(val) =>
              setFields((prevFields) =>
                prevFields.map((field) =>
                  field.name === name ? { ...field, value: val } : field
                )
              )
            }
            checked={value ? value : 0 }
          />
        ))}

        <button type="submit" disabled={mutation.isLoading}>
          {mutation.isLoading
            ? 'Loading...'
            : method === 'create'
            ? 'Create'
            : 'Update'}
        </button>

        <button type="button" onClick={() => onClose()}>
          Voltar
        </button>

        <p style={{ color: mutation.isError ? 'red' : 'green' }}>
          {mutation.isError
            ? `Error: ${mutation.error?.message || 'Unknown error'}`
            : mutation.isSuccess && 'Operation successful!'}
        </p>
      </form>
    </Modal>
  );
};

export default PopupSoftware;
