import React, { useState } from 'react';
import { useAiChat } from '../useAiChat';

interface FormField {
    id: string;
    label: string;
    placeholder: string;
    field_type: 'text' | 'number' | 'date' | 'boolean' | 'slider' | 'calendar' | 'dropdown' | 'multi_select' | 'file_upload' | 'rating' | 'range' | 'color_picker' | 'email';
    required: boolean;
    options?: string[];
    min_value?: number;
    max_value?: number;
    step?: number;
    default_value?: string;
    is_disabled?: boolean;
    is_readonly?: boolean;
}

interface DynamicFormData {
    form_name: string;
    form_description: string;
    form_fields: FormField[];
}

interface DynamicFormRendererProps {
    data: DynamicFormData;
    // onSubmit?: (formData: Record<string, any>) => void;
}

export const DynamicFormRenderer: React.FC<DynamicFormRendererProps> = ({ data }) => {
    const [formData, setFormData] = useState<Record<string, any>>({});
    const [errors, setErrors] = useState<Record<string, string>>({});
    const api = useAiChat();

    const handleInputChange = (fieldId: string, value: any) => {
        setFormData(prev => ({
            ...prev,
            [fieldId]: value
        }));

        // Clear error when user starts typing
        if (errors[fieldId]) {
            setErrors(prev => ({
                ...prev,
                [fieldId]: ''
            }));
        }
    };

    const validateForm = (): boolean => {
        const newErrors: Record<string, string> = {};

        data.form_fields.forEach(field => {
            if (field.required && (!formData[field.id] || formData[field.id] === '')) {
                newErrors[field.id] = `${field.label} is required`;
            }

            // Additional validation for specific field types
            if (field.field_type === 'email' && formData[field.id]) {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(formData[field.id])) {
                    newErrors[field.id] = 'Please enter a valid email address';
                }
            }

            if (field.field_type === 'number' && formData[field.id]) {
                const numValue = Number(formData[field.id]);
                if (isNaN(numValue)) {
                    newErrors[field.id] = 'Please enter a valid number';
                } else {
                    if (field.min_value !== undefined && numValue < field.min_value) {
                        newErrors[field.id] = `Value must be at least ${field.min_value}`;
                    }
                    if (field.max_value !== undefined && numValue > field.max_value) {
                        newErrors[field.id] = `Value must be at most ${field.max_value}`;
                    }
                }
            }
        });

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (validateForm()) {
            api.composer.send(
                `I have submitted the form with the following data: ${JSON.stringify(formData).replace(/"/g, '\\"')}`
            );
        }
    };

    const renderField = (field: FormField) => {
        const fieldValue = formData[field.id] ?? field.default_value ?? '';
        const fieldError = errors[field.id];
        const isDisabled = field.is_disabled || field.is_readonly;

        const commonFieldProps = {
            id: field.id,
            value: fieldValue,
            onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) =>
                handleInputChange(field.id, e.target.value),
            placeholder: field.placeholder,
            disabled: isDisabled,
            readOnly: field.is_readonly,
            style: {
                width: '94%',
                padding: '12px 16px',
                border: fieldError ? '1px solid #EF4444' : '1px solid #D1D5DB',
                borderRadius: '8px',
                fontSize: '14px',
                backgroundColor: isDisabled ? '#F3F4F6' : 'white',
                color: isDisabled ? '#6B7280' : '#374151',
                transition: 'all 0.2s ease'
            } as React.CSSProperties
        };

        switch (field.field_type) {
            case 'text':
            case 'email':
                return (
                    <input
                        type={field.field_type}
                        {...commonFieldProps}
                    />
                );

            case 'number':
                return (
                    <input
                        type="number"
                        min={field.min_value}
                        max={field.max_value}
                        step={field.step}
                        {...commonFieldProps}
                    />
                );

            case 'date':
                return (
                    <input
                        type="date"
                        {...commonFieldProps}
                    />
                );

            case 'boolean':
                return (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <input
                            type="checkbox"
                            id={field.id}
                            checked={Boolean(fieldValue)}
                            onChange={(e) => handleInputChange(field.id, e.target.checked)}
                            disabled={isDisabled}
                            style={{
                                width: '18px',
                                height: '18px',
                                accentColor: '#3B82F6'
                            }}
                        />
                        <label htmlFor={field.id} style={{ fontSize: '14px', color: '#374151' }}>
                            {field.label}
                        </label>
                    </div>
                );

            case 'dropdown':
                return (
                    <select {...commonFieldProps}>
                        <option value="">{field.placeholder}</option>
                        {field.options?.map((option, index) => (
                            <option key={index} value={option}>
                                {option}
                            </option>
                        ))}
                    </select>
                );

            case 'multi_select':
                return (
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                        {field.options?.map((option, index) => {
                            const isSelected = Array.isArray(fieldValue) && fieldValue.includes(option);
                            return (
                                <label
                                    key={index}
                                    style={{
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '6px',
                                        padding: '8px 12px',
                                        border: isSelected ? '1px solid #3B82F6' : '1px solid #D1D5DB',
                                        borderRadius: '20px',
                                        backgroundColor: isSelected ? 'rgba(59, 130, 246, 0.1)' : 'white',
                                        cursor: isDisabled ? 'not-allowed' : 'pointer',
                                        fontSize: '12px',
                                        color: isSelected ? '#2563eb' : '#374151',
                                        opacity: isDisabled ? 0.6 : 1
                                    }}
                                >
                                    <input
                                        type="checkbox"
                                        checked={isSelected}
                                        onChange={(e) => {
                                            const currentValues = Array.isArray(fieldValue) ? fieldValue : [];
                                            const newValues = e.target.checked
                                                ? [...currentValues, option]
                                                : currentValues.filter(v => v !== option);
                                            handleInputChange(field.id, newValues);
                                        }}
                                        disabled={isDisabled}
                                        style={{ display: 'none' }}
                                    />
                                    {option}
                                </label>
                            );
                        })}
                    </div>
                );

            case 'slider':
            case 'range':
                return (
                    <div>
                        <input
                            type="range"
                            min={field.min_value || 0}
                            max={field.max_value || 100}
                            step={field.step || 1}
                            value={fieldValue}
                            onChange={(e) => handleInputChange(field.id, e.target.value)}
                            disabled={isDisabled}
                            style={{
                                width: '100%',
                                height: '6px',
                                borderRadius: '3px',
                                background: '#D1D5DB',
                                outline: 'none',
                                opacity: isDisabled ? 0.6 : 1
                            }}
                        />
                        <div style={{
                            textAlign: 'center',
                            marginTop: '8px',
                            fontSize: '14px',
                            color: '#6B7280'
                        }}>
                            {fieldValue}
                        </div>
                    </div>
                );

            case 'rating':
                return (
                    <div style={{ display: 'flex', gap: '4px' }}>
                        {[1, 2, 3, 4, 5].map((star) => (
                            <button
                                key={star}
                                type="button"
                                onClick={() => handleInputChange(field.id, star)}
                                disabled={isDisabled}
                                style={{
                                    background: 'none',
                                    border: 'none',
                                    fontSize: '24px',
                                    cursor: isDisabled ? 'not-allowed' : 'pointer',
                                    color: Number(fieldValue) >= star ? '#F59E0B' : '#D1D5DB',
                                    opacity: isDisabled ? 0.6 : 1
                                }}
                            >
                                ⭐
                            </button>
                        ))}
                    </div>
                );

            case 'color_picker':
                return (
                    <input
                        type="color"
                        value={fieldValue || '#000000'}
                        onChange={(e) => handleInputChange(field.id, e.target.value)}
                        disabled={isDisabled}
                        style={{
                            width: '60px',
                            height: '40px',
                            border: '1px solid #D1D5DB',
                            borderRadius: '8px',
                            cursor: isDisabled ? 'not-allowed' : 'pointer',
                            opacity: isDisabled ? 0.6 : 1
                        }}
                    />
                );

            case 'file_upload':
                return (
                    <input
                        type="file"
                        onChange={(e) => {
                            const file = e.target.files?.[0];
                            handleInputChange(field.id, file);
                        }}
                        disabled={isDisabled}
                        style={{
                            width: '100%',
                            padding: '12px 16px',
                            border: '1px solid #D1D5DB',
                            borderRadius: '8px',
                            fontSize: '14px',
                            backgroundColor: isDisabled ? '#F3F4F6' : 'white',
                            color: isDisabled ? '#6B7280' : '#374151'
                        }}
                    />
                );

            default:
                return (
                    <input
                        type="text"
                        {...commonFieldProps}
                    />
                );
        }
    };

    return (
        <div style={{
            background: 'rgba(255, 255, 255, 0.95)',
            borderRadius: '16px',
            padding: '20px',
            margin: '12px 0',
            border: '1px solid rgba(0, 0, 0, 0.1)',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)'
        }}>
            <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                marginBottom: '16px'
            }}>
                <div style={{
                    width: '40px',
                    height: '40px',
                    borderRadius: '50%',
                    background: 'linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    fontSize: '18px'
                }}>
                    📝
                </div>
                <div>
                    <h3 style={{
                        margin: 0,
                        fontSize: '18px',
                        fontWeight: '600',
                        color: '#2d3748'
                    }}>
                        {data.form_name}
                    </h3>
                    {data.form_description && (
                        <p style={{
                            margin: '4px 0 0 0',
                            fontSize: '14px',
                            color: '#6B7280',
                            lineHeight: '1.4'
                        }}>
                            {data.form_description}
                        </p>
                    )}
                </div>
            </div>

            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                {data.form_fields.map((field) => (
                    <div key={field.id} style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                        {field.field_type !== 'boolean' && (
                            <label
                                htmlFor={field.id}
                                style={{
                                    fontSize: '14px',
                                    fontWeight: '500',
                                    color: '#374151',
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '4px'
                                }}
                            >
                                {field.label}
                                {field.required && (
                                    <span style={{ color: '#EF4444', fontSize: '12px' }}>*</span>
                                )}
                            </label>
                        )}

                        {renderField(field)}

                        {errors[field.id] && (
                            <div style={{
                                fontSize: '12px',
                                color: '#EF4444',
                                marginTop: '4px'
                            }}>
                                {errors[field.id]}
                            </div>
                        )}
                    </div>
                ))}

                <button
                    type="submit"
                    style={{
                        background: 'linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '8px',
                        padding: '12px 24px',
                        fontSize: '14px',
                        fontWeight: '600',
                        cursor: 'pointer',
                        transition: 'all 0.2s ease',
                        marginTop: '8px'
                    }}
                    onMouseEnter={(e) => {
                        e.currentTarget.style.transform = 'translateY(-1px)';
                        e.currentTarget.style.boxShadow = '0 4px 12px rgba(59, 130, 246, 0.3)';
                    }}
                    onMouseLeave={(e) => {
                        e.currentTarget.style.transform = 'translateY(0)';
                        e.currentTarget.style.boxShadow = 'none';
                    }}
                >
                    Submit Form
                </button>
            </form>
        </div>
    );
}; 