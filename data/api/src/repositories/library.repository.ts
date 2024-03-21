interface ILibraryRepository<LibraryRecord> {
    getAll: () => Promise<LibraryRecord[]>
    getSince: (since: string) => Promise<LibraryRecord[]>
    getRecent: (limit: number) => Promise<LibraryRecord[]>
    createRecord: (record: LibraryRecord) => Promise<LibraryRecord>
}

export default ILibraryRepository;