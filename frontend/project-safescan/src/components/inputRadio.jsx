import soft from '../assets/styles/Home/Soft.module.css';

const Radio = ({ pergunta, nome, value, onchange }) => {
    return (
        <div className={soft.formGroup}>
            <legend className={soft.titlePerg}>{pergunta}</legend>
            <div className={soft.radioGroup}>
                <input
                    type="radio"
                    className={soft.radioButton}
                    id={`software-${nome}-s`}
                    name={`software-${nome}`}
                    value={1}
                    onChange={(e) => onchange(parseInt(e.target.value))}
                    checked={value === 1 || value} // Verifica se o valor atual é 1
                />
                <label htmlFor={`software-${nome}-s`} className={soft.radioLabel}>
                    Sim
                </label>
                <input
                    type="radio"
                    className={soft.radioButton}
                    id={`software-${nome}-n`}
                    name={`software-${nome}`}
                    value={0}
                    onChange={(e) => onchange(parseInt(e.target.value))}
                    checked={value === 0 || !value} // Verifica se o valor atual é 0
                />
                <label htmlFor={`software-${nome}-n`} className={soft.radioLabel}>
                    Não
                </label>
                <button type="button" className={soft.editButton}><i className="bi-pencil-square"></i></button>
            </div>
        </div>
    );
};

export default Radio;
