
import { useEffect, useState, useMemo } from 'react';
import { getNotes } from './api';
import './PatientView.css';

const PatientView = ({ onLogout }) => {
    const [notes, setNotes] = useState([]);
    const [filter, setFilter] = useState('all');
    const [customRange, setCustomRange] = useState({ start: '', end: '' });
    const [activeTab, setActiveTab] = useState('notes');
    const [expandedNoteId, setExpandedNoteId] = useState(null);

    useEffect(() => {
        const fetchNotes = async () => {
            try {
                const data = await getNotes();
                setNotes(data);
            } catch (err) {
                console.error("Failed to fetch notes", err);
            }
        };
        fetchNotes();
    }, []);

    const timeAgo = (date) => {
        if (!date) return "";
        const seconds = Math.floor((new Date() - new Date(date)) / 1000);
        let interval = seconds / 31536000;
        if (interval > 1) return Math.floor(interval) + (Math.floor(interval) > 1 ? " years" : " year") + " ago";
        interval = seconds / 2592000;
        if (interval > 1) return Math.floor(interval) + (Math.floor(interval) > 1 ? " months" : " month") + " ago";
        interval = seconds / 86400;
        if (interval > 1) return Math.floor(interval) + (Math.floor(interval) > 1 ? " days" : " day") + " ago";
        interval = seconds / 3600;
        if (interval > 1) return Math.floor(interval) + (Math.floor(interval) > 1 ? " hours" : " hour") + " ago";
        interval = seconds / 60;
        if (interval > 1) return Math.floor(interval) + (Math.floor(interval) > 1 ? " minutes" : " minute") + " ago";
        return Math.floor(seconds) + " seconds ago";
    };

    const filteredNotes = useMemo(() => {
        const now = new Date();
        return notes.filter(noteItem => {
            const noteDate = new Date(noteItem.create_date);
            if (filter === 'today') {
                return noteDate.toDateString() === now.toDateString();
            } else if (filter === 'last_week') {
                const lastWeek = new Date();
                lastWeek.setDate(now.getDate() - 7);
                return noteDate >= lastWeek;
            } else if (filter === 'last_month') {
                const lastMonth = new Date();
                lastMonth.setMonth(now.getMonth() - 1);
                return noteDate >= lastMonth;
            } else if (filter === 'custom') {
                const start = customRange.start ? new Date(customRange.start) : null;
                const end = customRange.end ? new Date(customRange.end) : null;
                if (start && end) {
                    return noteDate >= start && noteDate <= end;
                }
                return true;
            }
            return true; // all
        }).sort((a, b) => new Date(b.create_date) - new Date(a.create_date));
    }, [notes, filter, customRange]);

    const stats = useMemo(() => {
        if (filteredNotes.length === 0) return { hourly: [], monthly: [], avgLength: 0 };

        const hourly = Array(24).fill(0);
        const monthlyData = {};
        let totalLength = 0;

        filteredNotes.forEach(noteItem => {
            const date = new Date(noteItem.create_date);
            hourly[date.getHours()] += 1;

            const month = date.getMonth();
            const year = date.getFullYear();
            if (!monthlyData[month]) monthlyData[month] = { sum: 0, years: new Set() };
            monthlyData[month].sum += 1;
            monthlyData[month].years.add(year);

            totalLength += noteItem.note ? noteItem.note.length : 0;
        });

        const monthly = Array(12).fill(0).map((_, i) => {
            if (monthlyData[i]) {
                return monthlyData[i].sum / monthlyData[i].years.size;
            }
            return 0;
        });

        return {
            hourly,
            monthly,
            avgLength: Math.round(totalLength / filteredNotes.length)
        };
    }, [filteredNotes]);

    const toggleExpand = (id) => {
        setExpandedNoteId(expandedNoteId === id ? null : id);
    };

    return (
        <div className="patient-view-container">
            <header>
                <h1>Patient Dashboard</h1>
                <button className="btn btn-secondary" onClick={onLogout}>Logout</button>
            </header>

            <div className="tabs-container">
                <button
                    className={`tab-btn ${activeTab === 'notes' ? 'active' : ''}`}
                    onClick={() => setActiveTab('notes')}
                >
                    My Notes
                </button>
                <button
                    className={`tab-btn ${activeTab === 'dashboard' ? 'active' : ''}`}
                    onClick={() => setActiveTab('dashboard')}
                >
                    Statistics
                </button>
            </div>

            <div className="filters-row">
                <select
                    value={filter}
                    onChange={(e) => setFilter(e.target.value)}
                >
                    <option value="all">All Time</option>
                    <option value="today">Today</option>
                    <option value="last_week">Last Week</option>
                    <option value="last_month">Last Month</option>
                    <option value="custom">Custom Range</option>
                </select>

                {filter === 'custom' && (
                    <div className="custom-dates">
                        <input
                            type="date"
                            value={customRange.start}
                            onChange={(e) => setCustomRange({ ...customRange, start: e.target.value })}
                        />
                        <span>-</span>
                        <input
                            type="date"
                            value={customRange.end}
                            onChange={(e) => setCustomRange({ ...customRange, end: e.target.value })}
                        />
                    </div>
                )}
            </div>

            {activeTab === 'notes' ? (
                <div className="notes-container">
                    {filteredNotes.map((noteItem, index) => (
                        <div key={index} className="note-item">
                            <div className="note-summary" onClick={() => toggleExpand(index)}>
                                <span>{noteItem.note.substring(0, 50)}{noteItem.note.length > 50 ? '...' : ''}</span>
                                <span className="arrow">{expandedNoteId === index ? '▲' : '▼'}</span>
                            </div>
                            {expandedNoteId === index && (
                                <div className="note-details">
                                    <p>{noteItem.note}</p>
                                    <div className="note-date">
                                        {timeAgo(noteItem.create_date)} ({new Date(noteItem.create_date).toLocaleString()})
                                    </div>
                                </div>
                            )}
                        </div>
                    ))}
                    {filteredNotes.length === 0 && <p style={{ textAlign: 'center', marginTop: '40px', color: '#999' }}>No data available for the selected range.</p>}
                </div>
            ) : (
                <div className="statistics-container">
                    <div className="stats-grid">
                        <div className="stat-card">
                            <h3>Total Notes</h3>
                            <div className="value">{filteredNotes.length}</div>
                        </div>
                        <div className="stat-card">
                            <h3>Avg Length</h3>
                            <div className="value">{stats.avgLength}</div>
                        </div>
                    </div>

                    <div className="chart-section">
                        <h3>Hourly Activity (Notes by Hour)</h3>
                        <div className="simple-chart">
                            {stats.hourly.map((count, hour) => {
                                const max = Math.max(...stats.hourly, 1);
                                return (
                                    <div key={hour} className="chart-column">
                                        <div
                                            className="chart-bar"
                                            style={{ height: `${(count / max) * 100}%` }}
                                            data-label={`${hour}:00 - ${count} notes`}
                                        ></div>
                                        <div className="chart-tick">{hour}</div>
                                    </div>
                                );
                            })}
                        </div>
                    </div>

                    <div className="chart-section">
                        <h3>Monthly Frequency (Avg)</h3>
                        <div className="simple-chart">
                            {['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'].map((m, i) => {
                                const max = Math.max(...stats.monthly, 1);
                                return (
                                    <div key={i} className="chart-column">
                                        <div
                                            className="chart-bar"
                                            style={{ height: `${(stats.monthly[i] / max) * 100}%` }}
                                            data-label={`${m} - ${stats.monthly[i].toFixed(1)} avg`}
                                        ></div>
                                        <div className="chart-tick">{m}</div>
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default PatientView;
