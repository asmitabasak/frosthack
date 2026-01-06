import { View, Text, FlatList, StyleSheet } from 'react-native';
import { useEffect, useState } from 'react';
import { fetchAlerts, Alert } from '../constants/api';

export default function Alerts() {
    const [alerts, setAlerts] = useState<Alert[]>([]);

    useEffect(() => {
        fetchAlerts().then(setAlerts).catch(console.error);
    }, []);

    const renderItem = ({ item }: { item: Alert }) => (
        <View style={[styles.card, { borderLeftColor: item.severity === 'Critical' ? '#ff4444' : '#FF9800' }]}>
            <View style={styles.header}>
                <Text style={[styles.severity, { color: item.severity === 'Critical' ? '#ff4444' : '#FF9800' }]}>{item.severity}</Text>
                <Text style={styles.time}>{item.timestamp}</Text>
            </View>
            <Text style={styles.desc}>{item.description}</Text>
            <Text style={styles.source}>Source: {item.source}</Text>
        </View>
    );

    return (
        <View style={styles.container}>
            <FlatList
                data={alerts}
                renderItem={renderItem}
                keyExtractor={item => String(item.id)}
                contentContainerStyle={{ padding: 20 }}
            />
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#f2f2f2' },
    card: { backgroundColor: 'white', padding: 15, marginBottom: 10, borderRadius: 10, elevation: 2, borderLeftWidth: 5 },
    header: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 5 },
    severity: { fontWeight: 'bold' },
    time: { color: '#999', fontSize: 12 },
    desc: { color: '#333', fontSize: 16, marginBottom: 5 },
    source: { color: '#666', fontStyle: 'italic', fontSize: 12 }
});