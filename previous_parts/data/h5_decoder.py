import os
import h5py

# Define the main directory path
main_dir = 'data/MillionSongSubset/'

def explore_h5_object(obj, indent=0):
    """Recursive function to explore datasets and groups in an HDF5 file."""
    for key in obj.keys():
        item = obj[key]
        print(" " * indent + f"Key: {key}")

        if isinstance(item, h5py.Dataset):
            # If it's a dataset, print shape and type, then sample data
            print(" " * (indent + 2) + f"Dataset: {key}")
            print(" " * (indent + 4) + "Shape:", item.shape)
            print(" " * (indent + 4) + "Data Type:", item.dtype)
            print(" " * (indent + 4) + "Sample data:\n", item[:10])  # Display first 10 entries if small enough

        elif isinstance(item, h5py.Group):
            # If it's a group, recurse into it
            print(" " * (indent + 2) + f"Group: {key}")
            explore_h5_object(item, indent + 4)  # Recurse into group

def process_h5_file(file_path):
    """Function to open and inspect .h5 file content."""
    with h5py.File(file_path, 'r') as hdf:
        print(f"Processing file: {file_path}")
        explore_h5_object(hdf)

def traverse_directories(main_dir):
    """Function to recursively navigate through directories and process each .h5 file."""
    for root, dirs, files in os.walk(main_dir):
        for file in files:
            if file.endswith('.h5'):
                file_path = os.path.join(root, file)
                process_h5_file(file_path)

# Run the traversal and processing function
traverse_directories(main_dir)