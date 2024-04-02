interface ILibraryPredRepository<LibraryPred> {
    updatePredictions: (predictions: LibraryPred[]) => Promise<LibraryPred[]>,
    getPredictions: () => Promise<LibraryPred[]>
}

export default ILibraryPredRepository;