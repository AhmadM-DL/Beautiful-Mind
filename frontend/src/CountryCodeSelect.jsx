import { useState, useRef, useEffect } from 'react';
import { countryCodes } from './countryCodes';
import './CountryCodeSelect.css';

const CountryCodeSelect = ({ value, onChange }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [searchTerm, setSearchTerm] = useState('');
    const dropdownRef = useRef(null);

    // Filter countries based on search term
    const filteredCountries = countryCodes.filter(country =>
        country.country.toLowerCase().includes(searchTerm.toLowerCase()) ||
        country.code.includes(searchTerm)
    );

    // Close dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setIsOpen(false);
                setSearchTerm('');
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const handleSelect = (code) => {
        onChange(code);
        setIsOpen(false);
        setSearchTerm('');
    };

    const selectedCountry = countryCodes.find(c => c.code === value);

    return (
        <div className="country-code-select" ref={dropdownRef}>
            <button
                type="button"
                className="country-code-button"
                onClick={() => setIsOpen(!isOpen)}
            >
                <span>{value}</span>
                <span className="arrow">{isOpen ? '▲' : '▼'}</span>
            </button>

            {isOpen && (
                <div className="country-code-dropdown">
                    <input
                        type="text"
                        className="country-code-search"
                        placeholder="Search country..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        autoFocus
                    />
                    <div className="country-code-list">
                        {filteredCountries.length > 0 ? (
                            filteredCountries.map((country) => (
                                <div
                                    key={country.code + country.country}
                                    className={`country-code-item ${country.code === value ? 'selected' : ''}`}
                                    onClick={() => handleSelect(country.code)}
                                >
                                    <span className="country-name">{country.country}</span>
                                    <span className="country-code">{country.code}</span>
                                </div>
                            ))
                        ) : (
                            <div className="no-results">No countries found</div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default CountryCodeSelect;
