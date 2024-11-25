const Radio = ({ pergunta, nome, value, onchange }) => {
    return (
        <fieldset>
            <legend>{pergunta}</legend>
            <div>
                <input
                    type="radio"
                    id={`software-${nome}-s`}
                    name={`software-${nome}`}
                    value={1}
                    onChange={(e) => onchange(parseInt(e.target.value))}
                    checked={value === 1}
                />
                <label htmlFor={`software-${nome}-s`}>Sim</label>
            </div>
            <div>
                <input
                    type="radio"
                    id={`software-${nome}-n`}
                    name={`software-${nome}`}
                    value={0}
                    onChange={(e) => onchange(parseInt(e.target.value))}
                    checked={value === 0}
                />
                <label htmlFor={`software-${nome}-n`}>Não</label>
            </div>
        </fieldset>
    );
};

export default Radio;
