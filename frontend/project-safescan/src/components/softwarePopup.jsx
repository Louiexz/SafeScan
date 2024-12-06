import React, { useEffect, useState } from 'react';
import { createSoftware, updateSoftware } from '../services/softwareService';
import Radio from './inputRadio';
import { useMutation } from 'react-query';
import Modal from 'react-modal'; // Biblioteca para modal
import soft from '../assets/styles/Home/Soft.module.css'

const PopupSoftware = ({ method, data, onClose, softName, refetch }) => {
  const [softwareName, setSoftwareName] = useState("");
  const [fields, setFields] = useState([
    { name: "localizacao", label: "Location?", value: false },
    { name: "armazenamento", label: "External storage?", value: false },
    { name: "bluetooth", label: "Bluetooth?", value: false },
    { name: "biblioteca_classes", label: "Code execution?", value: false },
    { name: "midia_audio", label: "Audio recording or vibration?", value: false },
    { name: "rede", label: "Network?", value: false },
    { name: "sistema", label: "Messages?", value: false },
    { name: "message", label: "Modifications to the system and process control?", value: false },
    { name: "pacotes", label: "Packages?", value: false },
  ]);

  const mutationCreateSoftware = useMutation(createSoftware, {
    onSuccess: () => {
      {refetch ? refetch() : null }
      console.log('Software created succesfully');
    },
    onError: (error) => console.error('Erro creating software:', error),
  });

  const mutationUpdateSoftware = useMutation(updateSoftware, {
    onSuccess: () => {
      {refetch ? refetch() : null }
      console.log('Software updated succesfully');
    },
    onError: (error) => console.error('Erro updating software:', error),
  });

  const getMutationState = (method) =>
    method === 'create' ? mutationCreateSoftware : mutationUpdateSoftware;

  const [feedbackMessage, setFeedbackMessage] = useState(null);
  const [feedbackType, setFeedbackType] = useState(null); // 'success' ou 'error'

  const handleSubmit = (event) => {
    event.preventDefault();
    setFeedbackMessage(null); // Reseta mensagem ao submeter

    if (!softwareName || fields.some(field => field.value === null || field.value === "")) {
      setFeedbackMessage("Please write all fields.");
      setFeedbackType("error");
      return;
    }

    const dataToSend = {
      name: softwareName,
      ...Object.fromEntries(fields.map(({ name, value }) => [name, value ? 1 : 0])),
    };

    if (method === "update" && data) {
      dataToSend.id = data.id;
    }

    const mutation = method === "create"
      ? mutationCreateSoftware
      : mutationUpdateSoftware;

    mutation.mutate(dataToSend, {
      onSuccess: () => {
        setFeedbackMessage("Operation succesfully!");
        setFeedbackType("success");
        onClose();
      },
      onError: (error) => {
        setFeedbackMessage(`Error: ${error.message}`);
        setFeedbackType("error");
      },
    });
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
      style={{
        overlay: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)', // Fundo semi-transparente
        },
        content: {
          background: 'transparent', // Cor do conteúdo do modal
          border: 'transparent',
          padding: '20px',
          maxWidth: '500px',
          margin: 'auto',
        },
      }}
    >
      <div className={soft.popupPerfil}>
        <form onSubmit={handleSubmit} id="form" className={soft.popupFormPerfil}>
          <div className={soft.groupPerfil}>
            <label className={soft.titlePerg} htmlFor="name">Software name</label>
            <div className={soft.inputPerfil}>
              <input
                type="text"
                id="name"
                value={softwareName}
                placeholder="Enter the name of the software"
                onChange={(e) => setSoftwareName(e.target.value)}
              />
            </div>
          </div>

          {fields.map(({ name, label, value }) => (
            <div key={name} className={soft.formGrid}>
              <div className={soft.formGroup}>
                <Radio
                  pergunta={label}
                  nome={name}
                  value={value}
                  softName={softName}
                  onchange={(val) =>
                    setFields((prevFields) =>
                      prevFields.map((field) =>
                        field.name === name ? { ...field, value: val } : field
                      )
                    )
                  }
                  checked={value ? value : 0}
                />
              </div>
            </div>
          ))}

          <div className={soft.formActions}>
            <button className={soft.saveButton} type="submit" disabled={mutation.isLoading}>
              {mutation.isLoading
                ? 'Loading...'
                : method === 'create'
                ? 'Create'
                : 'Update'}
            </button>
            <button className={soft.saveButton} type="button"
              onClick={onClose}
              disabled={mutation.isLoading}>
              Back
            </button>
          </div>

          {feedbackMessage && (
            <p className={soft.message} style={{ color: feedbackType === 'error' ? 'red' : 'green' }}>
              {feedbackMessage}
            </p>
          )}
        </form>
      </div>
    </Modal>
  );
};

export default PopupSoftware;
