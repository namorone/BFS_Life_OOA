import { useEffect, useState } from "react";
import "./CategoriesPage.css";

export default function CategoriesPage() {
  const [categories, setCategories] = useState([]);
  const [modalType, setModalType] = useState(null); // add | edit | delete | null
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [inputValue, setInputValue] = useState("");

  const load = () => {
    fetch("http://localhost:8000/api/v1/categories")
      .then((r) => r.json())
      .then(setCategories);
  };

  useEffect(() => {
    load();
  }, []);

  const openAddModal = () => {
    setInputValue("");
    setSelectedCategory(null);
    setModalType("add");
  };

  const openEditModal = (category) => {
    setSelectedCategory(category);
    setInputValue(category.name);
    setModalType("edit");
  };

  const openDeleteModal = (category) => {
    setSelectedCategory(category);
    setModalType("delete");
  };

  const closeModal = () => {
    setModalType(null);
    setSelectedCategory(null);
    setInputValue("");
  };

  const handleAdd = async () => {
    if (!inputValue.trim()) return;

    await fetch("http://localhost:8000/api/v1/categories", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: inputValue }),
    });

    closeModal();
    load();
  };

  const handleEdit = async () => {
    if (!inputValue.trim() || !selectedCategory) return;

    await fetch(`http://localhost:8000/api/v1/categories/${selectedCategory.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: inputValue }),
    });

    closeModal();
    load();
  };

  const handleDelete = async () => {
    if (!selectedCategory) return;

    await fetch(`http://localhost:8000/api/v1/categories/${selectedCategory.id}`, {
      method: "DELETE",
    });

    closeModal();
    load();
  };

  return (
    <div className="categories-page">
      <div className="categories-header">
        <a href="/settings" className="back-link">← Back to Settings</a>
        <h2>Manage Categories</h2>
        <p>Organize your inventory with custom categories</p>
      </div>

      <div className="categories-card">
        <div className="categories-card-top">
          <div>
            <h3>Inventory Categories</h3>
            <p>{categories.length} categories available</p>
          </div>
          <button className="primary-button" onClick={openAddModal}>
            + Add Category
          </button>
        </div>

        <div className="categories-list">
          {categories.map((category) => (
            <div key={category.id} className="category-row">
              <div className="category-info">
                <div className="category-icon">📁</div>
                <div>
                  <div className="category-name">{category.name}</div>
                  <div className="category-meta">Custom category</div>
                </div>
              </div>

              <div className="category-actions">
                <button
                  className="icon-button"
                  onClick={() => openEditModal(category)}
                >
                  ✏️
                </button>
                <button
                  className="icon-button delete"
                  onClick={() => openDeleteModal(category)}
                >
                  🗑️
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {modalType && (
        <div className="modal-overlay">
          <div className="modal">
            {modalType === "add" && (
              <>
                <h3>Add New Category</h3>
                <p>Create a new category to organize your inventory items</p>

                <label>Category Name</label>
                <input
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="e.g., Kitchen Appliances"
                />

                <div className="modal-actions">
                  <button className="secondary-button" onClick={closeModal}>
                    Cancel
                  </button>
                  <button className="primary-button" onClick={handleAdd}>
                    Add Category
                  </button>
                </div>
              </>
            )}

            {modalType === "edit" && (
              <>
                <h3>Edit Category</h3>
                <p>Update the category name</p>

                <label>Category Name</label>
                <input
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                />

                <div className="modal-actions">
                  <button className="secondary-button" onClick={closeModal}>
                    Cancel
                  </button>
                  <button className="primary-button" onClick={handleEdit}>
                    Save Changes
                  </button>
                </div>
              </>
            )}

            {modalType === "delete" && (
              <>
                <h3>Delete Category</h3>
                <p>
                  Are you sure you want to delete{" "}
                  <strong>{selectedCategory?.name}</strong>?
                </p>

                <div className="modal-actions">
                  <button className="secondary-button" onClick={closeModal}>
                    Cancel
                  </button>
                  <button className="danger-button" onClick={handleDelete}>
                    Delete
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
