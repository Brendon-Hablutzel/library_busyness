import { Library } from "./models";

interface LibrarySelectorProps {
    setCurrentLibrary: (library: Library) => void
}

const LibrarySelector = ({ setCurrentLibrary }: LibrarySelectorProps) => {

    return (
        <div id="library-header">
            <select onChange={e => {
                let library = e.target.value;
                if (library === "hill" || library === "hunt") {
                    setCurrentLibrary(library);
                } else {
                    alert("invalid library");
                }
            }} id="library-selector">
                <option value="hunt">Hunt</option>
                <option value="hill">Hill</option>
            </select>
        </div>
    );
}

export default LibrarySelector;