const Radio = ({ pergunta, nome, value, onchange }) => {
    return (
        <fieldset>
            <legend>{pergunta}</legend>
            <div>
                <input
                type="radio"
                className={`software-${nome}-s`}
                id={`software-${nome}-s`}
                name={`software-${nome}`}
                value={1}
                onChange={(e) => onchange(parseInt(e.target.value))}
                checked={value === 1 || value } // Verifica se o valor atual é 1
                />
                <label htmlFor={`software-${nome}-s`}>Sim</label>
            </div>
            <div>
                <input
                type="radio"
                className={`software-${nome}-n`}
                id={`software-${nome}-n`}
                name={`software-${nome}`}
                value={0}
                onChange={(e) => onchange(parseInt(e.target.value))}
                checked={value === 0 || !value} // Verifica se o valor atual é 0
                />
                <label htmlFor={`software-${nome}-n`}>Não</label>
            </div>
        </fieldset>
    );
};

export default Radio;
