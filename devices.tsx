import { View, Text, FlatList, StyleSheet, Pressable } from 'react-native';
import { useRouter } from 'expo-router';
import { useEffect, useState } from 'react';
import { fetchDevices, Device } from '../constants/api';

export default function Devices() {
    const [devices, setDevices] = useState<Device[]>([]);
    const router = useRouter();

    useEffect(() => {
        fetchDevices().then(setDevices).catch(console.error);
    }, []);

    const renderItem = ({ item }: { item: Device }) => (
        <Pressable style={styles.card} onPress={() => router.push(`/device/${item.id}`)}>
            <View style={styles.row}>
                <Text style={styles.name}>{item.device_type}</Text>
                <View style={[styles.badge, { backgroundColor: item.status === 'Isolated' ? '#999' : (item.risk_score > 5 ? '#ff4444' : '#00C851') }]}>
                    <Text style={styles.badgeText}>{item.status}</Text>
                </View>
            </View>
            <Text style={styles.ip}>{item.ip_address}</Text>
            <Text style={styles.risk}>Risk Score: {item.risk_score}/10</Text>
        </Pressable>
    );

    return (
        <View style={styles.container}>
            <FlatList
                data={devices}
                renderItem={renderItem}
                keyExtractor={item => item.id}
                contentContainerStyle={{ padding: 20 }}
            />
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#f2f2f2' },
    card: { backgroundColor: 'white', padding: 15, marginBottom: 10, borderRadius: 10, elevation: 2 },
    row: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 5 },
    name: { fontSize: 18, fontWeight: 'bold', color: '#333' },
    ip: { color: '#666', marginBottom: 5 },
    risk: { fontWeight: 'bold', color: '#333' },
    badge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 12 },
    badgeText: { color: 'white', fontSize: 12, fontWeight: 'bold' }
});