import soft from '../assets/styles/Home/Soft.module.css'

const Radio = ({ pergunta, nome, softName, value, onchange }) => {
    return (
        <fieldset>
            <legend>{pergunta}</legend>
            <div>
                <input
                type="radio"
                className={soft.radioButton}
                id={`software-${nome}-${softName}-s`}
                name={`software-${nome}`}
                value={1}
                onChange={(e) => onchange(parseInt(e.target.value))}
                checked={value === 1 || value } // Verifica se o valor atual é 1
                />
                <label htmlFor={`software-${nome}-${softName}-s`} className={soft.radioLabel}>
                    Yes
                </label>
                <input
                type="radio"
                className={soft.radioButton}
                id={`software-${nome}-${softName}-n`}
                name={`software-${nome}`}
                value={0}
                onChange={(e) => onchange(parseInt(e.target.value))}
                checked={value === 0 || !value} // Verifica se o valor atual é 0
                />
                <label htmlFor={`software-${nome}-${softName}-n`} className={soft.radioLabel}>
                    No
                </label>
                <button type="button" className={soft.editButton}><i className="bi-pencil-square"></i></button>
            </div>
        </fieldset>
    );
};

export default Radio;
