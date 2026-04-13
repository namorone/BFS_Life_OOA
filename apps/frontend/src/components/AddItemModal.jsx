import { useEffect, useMemo, useState } from "react";

const initialForm = {
  name: "",
  categoryId: "",
  purchaseDate: "",
  purchasePrice: "",
  description: "",
  photo: null,
  hasWarranty: false,
  warrantyProvider: "",
  warrantyExpiryDate: "",
  warrantyNotes: "",
};

export default function AddItemModal({ open, categories, onClose, onSave, saving }) {
  const [form, setForm] = useState(initialForm);
  const [error, setError] = useState("");

  const selectedFileName = useMemo(
    () => form.photo?.name || "Upload Photo",
    [form.photo]
  );

  useEffect(() => {
    if (open) {
      setError("");
    }
  }, [open]);

  if (!open) {
    return null;
  }

  const updateField = (field) => (event) => {
    const value =
      field === "photo" ? event.target.files?.[0] || null : event.target.value;

    setForm((current) => ({ ...current, [field]: value }));
  };

  const toggleWarranty = () => {
    setForm((current) => ({
      ...current,
      hasWarranty: !current.hasWarranty,
      warrantyProvider: current.hasWarranty ? "" : current.warrantyProvider,
      warrantyExpiryDate: current.hasWarranty ? "" : current.warrantyExpiryDate,
      warrantyNotes: current.hasWarranty ? "" : current.warrantyNotes,
    }));
  };

  const handleClose = () => {
    setForm(initialForm);
    setError("");
    onClose();
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");

    if (!form.name.trim()) {
      setError("Inventory name is required.");
      return;
    }

    if (form.hasWarranty && !form.warrantyExpiryDate) {
      setError("Warranty expiry date is required when warranty is enabled.");
      return;
    }

    try {
      await onSave(form);
      setForm(initialForm);
    } catch (submitError) {
      setError(submitError.message || "Failed to save item.");
    }
  };

  return (
    <div className="modal-overlay" role="presentation">
      <div className="modal-card">
        <button type="button" className="modal-close" onClick={handleClose}>
          ×
        </button>

        <h2 className="modal-title">Add New Item</h2>

        <form className="item-form" onSubmit={handleSubmit}>
          <label className="form-field">
            <span className="form-label">Photo</span>
            <div className="upload-row">
              <label className="upload-button action-like-button">
                <input type="file" accept="image/*" onChange={updateField("photo")} hidden />
                {selectedFileName}
              </label>
            </div>
          </label>

          <label className="form-field">
            <span className="form-label">Inventory Name</span>
            <input
              type="text"
              placeholder="New Inventory Name"
              value={form.name}
              onChange={updateField("name")}
            />
          </label>

          <label className="form-field">
            <span className="form-label">Category</span>
            <select
              value={form.categoryId}
              onChange={updateField("categoryId")}
              className={!form.categoryId ? "is-placeholder" : ""}
            >
              <option value="">Select Category</option>
              {categories.map((category) => (
                <option key={category.id} value={category.id}>
                  {category.name}
                </option>
              ))}
            </select>
          </label>

          <label className="form-field">
            <span className="form-label">Purchase Date</span>
            <input
              type="date"
              value={form.purchaseDate}
              onChange={updateField("purchaseDate")}
              className={!form.purchaseDate ? "is-placeholder date-empty" : ""}
            />
          </label>

          <label className="form-field">
            <span className="form-label">Purchase Price</span>
            <input
              type="number"
              min="0"
              step="0.01"
              placeholder="xxxx"
              value={form.purchasePrice}
              onChange={updateField("purchasePrice")}
            />
          </label>

          <label className="form-field">
            <span className="form-label">Description</span>
            <textarea
              placeholder="Item Description"
              value={form.description}
              onChange={updateField("description")}
              rows={3}
            />
          </label>

          <button
            type="button"
            className="secondary-action action-like-button"
            onClick={toggleWarranty}
          >
            {form.hasWarranty ? "Remove Warranty" : "Add Warranty"}
          </button>

          {form.hasWarranty ? (
            <div className="warranty-box">
              <label className="form-field">
                <span className="form-label">Warranty Provider</span>
                <input
                  type="text"
                  placeholder="Store / manufacturer"
                  value={form.warrantyProvider}
                  onChange={updateField("warrantyProvider")}
                />
              </label>

              <label className="form-field">
                <span className="form-label">Warranty Expiry Date</span>
                <input
                  type="date"
                  value={form.warrantyExpiryDate}
                  onChange={updateField("warrantyExpiryDate")}
                  className={!form.warrantyExpiryDate ? "is-placeholder date-empty" : ""}
                />
              </label>

              <label className="form-field">
                <span className="form-label">Warranty Notes</span>
                <textarea
                  rows={2}
                  placeholder="Warranty notes"
                  value={form.warrantyNotes}
                  onChange={updateField("warrantyNotes")}
                />
              </label>
            </div>
          ) : null}

          {error ? <p className="form-error">{error}</p> : null}

          <div className="modal-actions">
            <button type="button" className="ghost-button" onClick={handleClose}>
              Cancel
            </button>
            <button type="submit" className="primary-button" disabled={saving}>
              {saving ? "Saving..." : "Save"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}